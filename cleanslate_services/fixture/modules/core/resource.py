"""Add interfaces for defining a resource."""

from abc import ABC, abstractmethod
from typing import Any


class IResource(ABC):

    """Interface for a resource."""

    @property
    def identifier(self):
        """Get unique id for the resource."""

    @abstractmethod
    def get_type(self):
        """Inspect the type for the underlying resource."""


class IScalar(ABC):

    """Represents immutable, raw data that be serialilzed and deserialized."""

    @abstractmethod
    def get_raw_bytes(self) -> bytes:
        """Get value or raw bytes."""


class IPyObject(ABC):

    """Python object as a resource."""

    @abstractmethod
    def instance(self) -> Any:
        """Get underlying instance of the resource."""


class DocumentResource(IScalar):

    """Documents as resources, constrained to size of 4kb."""


class JsonResource(IResource, DocumentResource):

    """Resource with JSON content."""
