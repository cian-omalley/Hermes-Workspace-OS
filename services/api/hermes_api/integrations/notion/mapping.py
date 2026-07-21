"""Declarative entity ↔ Notion database mappings.

Milestone 4 maps Projects and Tasks (the exit-criteria entities). The remaining Notion
databases from ``docs/07-NOTION_INTEGRATION.md`` follow the same pattern — add an
``EntityMapping`` and register it here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class Direction(StrEnum):
    BOTH = "both"
    OUT = "out"  # Hermes → Notion only
    IN = "in"  # Notion → Hermes only


@dataclass(frozen=True)
class FieldMap:
    hermes_attr: str
    notion_prop: str
    direction: Direction = Direction.BOTH


@dataclass(frozen=True)
class EntityMapping:
    entity_type: str
    # Key in ``integration.config['databases']`` holding this database's Notion id.
    database_key: str
    title_property: str
    fields: list[FieldMap] = field(default_factory=list)
    hermes_id_property: str = "hermes_id"

    def out_fields(self) -> list[FieldMap]:
        return [f for f in self.fields if f.direction in (Direction.BOTH, Direction.OUT)]

    def in_fields(self) -> list[FieldMap]:
        return [f for f in self.fields if f.direction in (Direction.BOTH, Direction.IN)]


PROJECT_MAPPING = EntityMapping(
    entity_type="project",
    database_key="projects",
    title_property="Name",
    fields=[
        FieldMap("name", "Name", Direction.BOTH),
        FieldMap("status", "Status", Direction.BOTH),
        FieldMap("key", "Key", Direction.OUT),
    ],
)

TASK_MAPPING = EntityMapping(
    entity_type="task",
    database_key="tasks",
    title_property="Title",
    fields=[
        FieldMap("title", "Title", Direction.BOTH),
        FieldMap("status", "Status", Direction.BOTH),
        FieldMap("priority", "Priority", Direction.BOTH),
    ],
)

MAPPINGS: dict[str, EntityMapping] = {
    PROJECT_MAPPING.entity_type: PROJECT_MAPPING,
    TASK_MAPPING.entity_type: TASK_MAPPING,
}
