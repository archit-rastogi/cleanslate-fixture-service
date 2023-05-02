from pydantic import BaseModel


class TestSessionRequest(BaseModel):

    """Pydantic test session model."""

    name: str
    description: str


class CreateFixtureInstanceRequest(BaseModel):

    """Request for creating a new fixture instance."""

    namespace: str
    name: str

class DeleteFixtureInstanceRequest(BaseModel):

    """Request to delete an existing fixture instance."""

    identifier: str


class CreateResourceRequest(BaseModel):

    """Request for creating a resource type."""

    resource_type: int
    content: str


class ResourceQuery(BaseModel):

    """Get Resource query params."""

    identifier: str | None = None


class GetResourceRequest(BaseModel):

    """Request to get a resource."""

    query: ResourceQuery


class DeleteResourceRequest(BaseModel):

    """Request to delete a resource."""

    identifier: str
