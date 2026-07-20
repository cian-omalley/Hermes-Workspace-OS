"""Services for the simple workspace-scoped content entities.

Each is a thin subclass of the generic ``CrudService`` — the whole point of the base is
that these need no bespoke logic beyond naming their model.
"""

from __future__ import annotations

from hermes_api.models.agent import Agent
from hermes_api.models.asset import Asset
from hermes_api.models.document import Document
from hermes_api.models.repository import Repository
from hermes_api.models.research import ResearchItem
from hermes_api.services.crud import CrudService


class DocumentService(CrudService[Document]):
    model = Document
    entity_name = "Document"


class ResearchService(CrudService[ResearchItem]):
    model = ResearchItem
    entity_name = "Research item"


class RepositoryService(CrudService[Repository]):
    model = Repository
    entity_name = "Repository"


class AssetService(CrudService[Asset]):
    model = Asset
    entity_name = "Asset"


class AgentService(CrudService[Agent]):
    model = Agent
    entity_name = "Agent"
