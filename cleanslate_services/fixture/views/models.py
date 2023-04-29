from pydantic import BaseModel


class TestSessionRequest(BaseModel):

    """Pydantic test session model."""

    name: str
    description: str


class CreateFixtureInstanceRequest(BaseModel):

    """Request for creating a new fixture instance."""

    namespace: str
    name: str
    session_id: int


class CreateResourceRequest(BaseModel):

    """Request for creating a resource type."""

    resource_type: int
    content: str
