"""Notion sync engine: outbound (Hermes → Notion) and inbound (Notion → Hermes).

Idempotent and conflict-aware. Conflict policy is **Hermes wins**: an inbound change is
applied only if the Hermes record has not changed since the last sync (detected by
comparing checksums); otherwise Hermes's value is kept and the conflict is logged. All
work happens inside the caller's unit of work.
"""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass
from typing import Any

from hermes_api.db import Base
from hermes_api.integrations.notion.client import NotionClient
from hermes_api.integrations.notion.mapping import MAPPINGS, EntityMapping
from hermes_api.models.integration import Integration
from hermes_api.models.project import Project
from hermes_api.models.sync import SyncLog, SyncState
from hermes_api.models.task import Task
from hermes_api.uow import UnitOfWork

_MODELS: dict[str, type[Base]] = {"project": Project, "task": Task}


@dataclass(frozen=True)
class SyncSummary:
    created: int = 0
    updated: int = 0
    unchanged: int = 0
    conflicts: int = 0

    def with_action(self, action: str) -> SyncSummary:
        return SyncSummary(
            created=self.created + (action == "created"),
            updated=self.updated + (action == "updated"),
            unchanged=self.unchanged + (action == "unchanged"),
            conflicts=self.conflicts + (action == "conflict"),
        )


class NotionSyncEngine:
    def __init__(self, uow: UnitOfWork, client: NotionClient, integration: Integration) -> None:
        self.uow = uow
        self.client = client
        self.integration = integration
        self.states = uow.repo_for(SyncState)

    # --- helpers ----------------------------------------------------------------------

    def _database_id(self, mapping: EntityMapping) -> str:
        databases = self.integration.config.get("databases", {})
        db_id = databases.get(mapping.database_key)
        if not db_id:
            raise ValueError(f"No Notion database configured for '{mapping.database_key}'")
        return str(db_id)

    @staticmethod
    def _mapped_properties(mapping: EntityMapping, entity: Any) -> dict[str, str]:
        props = {f.notion_prop: str(getattr(entity, f.hermes_attr)) for f in mapping.out_fields()}
        props[mapping.hermes_id_property] = str(entity.id)
        return props

    @staticmethod
    def _checksum(properties: dict[str, str]) -> str:
        payload = " ".join(f"{k}={v}" for k, v in sorted(properties.items()))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def _get_state(self, entity_type: str, hermes_id: uuid.UUID) -> SyncState | None:
        for state in self.states.list(
            integration_id=self.integration.id, entity_type=entity_type, hermes_id=hermes_id
        ):
            return state
        return None

    def _state_by_external(self, external_id: str) -> SyncState | None:
        for state in self.states.list(integration_id=self.integration.id, external_id=external_id):
            return state
        return None

    def _log(self, direction: str, entity_type: str | None, action: str, detail: str) -> None:
        self.uow.repo_for(SyncLog).add(
            SyncLog(
                integration_id=self.integration.id,
                direction=direction,
                entity_type=entity_type,
                action=action,
                detail=detail,
            )
        )

    # --- outbound ---------------------------------------------------------------------

    def sync_out_entity(self, entity_type: str, entity: Any) -> str:
        mapping = MAPPINGS[entity_type]
        props = self._mapped_properties(mapping, entity)
        checksum = self._checksum(props)
        state = self._get_state(entity_type, entity.id)

        if state is None:
            external_id = self.client.create_page(
                self._database_id(mapping), mapping.title_property, props
            )
            self.states.add(
                SyncState(
                    integration_id=self.integration.id,
                    entity_type=entity_type,
                    hermes_id=entity.id,
                    external_id=external_id,
                    checksum=checksum,
                )
            )
            action = "created"
        elif state.checksum != checksum:
            assert state.external_id is not None
            self.client.update_page(state.external_id, mapping.title_property, props)
            state.checksum = checksum
            self.states.add(state)
            action = "updated"
        else:
            action = "unchanged"

        self._log("outbound", entity_type, action, f"{entity_type}:{entity.id}")
        return action

    def sync_all_out(self, workspace_id: uuid.UUID) -> SyncSummary:
        summary = SyncSummary()
        for entity_type, model in _MODELS.items():
            for entity in self.uow.repo_for(model).list(workspace_id=workspace_id):
                summary = summary.with_action(self.sync_out_entity(entity_type, entity))
        return summary

    # --- inbound ----------------------------------------------------------------------

    def apply_inbound(self, external_id: str, external_properties: dict[str, str]) -> str:
        state = self._state_by_external(external_id)
        if state is None:
            # A Notion page with no Hermes counterpart. Creating Hermes records from
            # Notion-native pages is a later enhancement; for now, record and skip.
            self._log("inbound", None, "unmatched", external_id)
            return "unmatched"

        model = _MODELS[state.entity_type]
        entity = self.uow.repo_for(model).get(state.hermes_id)
        if entity is None:
            self._log("inbound", state.entity_type, "missing", str(state.hermes_id))
            return "missing"

        mapping = MAPPINGS[state.entity_type]
        current_checksum = self._checksum(self._mapped_properties(mapping, entity))
        if current_checksum != state.checksum:
            # Hermes changed since the last sync → Hermes wins.
            self._log("inbound", state.entity_type, "conflict", str(state.hermes_id))
            return "conflict"

        changed = False
        for field_map in mapping.in_fields():
            if field_map.notion_prop in external_properties:
                value = external_properties[field_map.notion_prop]
                if str(getattr(entity, field_map.hermes_attr)) != value:
                    setattr(entity, field_map.hermes_attr, value)
                    changed = True

        if not changed:
            self._log("inbound", state.entity_type, "unchanged", str(state.hermes_id))
            return "unchanged"

        self.uow.repo_for(model).add(entity)
        state.checksum = self._checksum(self._mapped_properties(mapping, entity))
        self.states.add(state)
        self._log("inbound", state.entity_type, "applied", str(state.hermes_id))
        return "applied"
