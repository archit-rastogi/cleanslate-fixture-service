"""Runner to execute a remote fixture."""

import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, ClassVar, Dict

import fixture.modules.api as api_lib
from fixture.modules.core.base import RemoteFixtureImplBase

LOGGER = logging.getLogger(__name__)


class FixtureType(Enum):

    """Types of fixtures."""

    FIXTURE_INTERNAL = 1
    FIXTURE_GITHUB = 2
    FIXTURE_DOCKER = 3


class RemoteFixtureContext(Enum):

    """Enum to capture the request context."""

    FIXTURE_TYPE = 1
    TEST_SESSION_ID = 2
    REMOTE_FIXTURE_SCOPE = 3


class RemoteFixtureRequest:

    """Class for the remote fixture request."""

    def __init__(self, namespace, name, context):
        self.namespace = namespace
        self.name = name
        self.context: Dict[RemoteFixtureContext, Any] = context


class FixtureInstance(ABC):

    """A resolved instance of fixture."""

    def __init__(
            self,
            fixture_type: FixtureType,
            fixture_class: ClassVar[RemoteFixtureImplBase],
            fixture_init_args: Dict[str, Any]):
        self.fixture_type = fixture_type
        self.fixture_class: ClassVar[RemoteFixtureImplBase] = fixture_class
        self.fixture_init_args = fixture_init_args

    @abstractmethod
    def create(self) -> RemoteFixtureImplBase:
        """Create an instance of fixture."""


class InternalFixtureInstance(FixtureInstance):

    """A resolved internal fixture instance."""

    def __init__(self, fixture_class: ClassVar[RemoteFixtureImplBase], fixture_init_args: Dict[str, Any]):
        super().__init__(FixtureType.FIXTURE_INTERNAL, fixture_class, fixture_init_args)

    def create(self) -> RemoteFixtureImplBase:
        """Creates an instance of remote fixture impl."""
        return self.fixture_class(self.fixture_init_args)


class RemoteFixtureLoader(ABC):

    """An Abstract remote fixture."""

    def __init__(self, fixture_request: RemoteFixtureRequest):
        self.fixture_request = fixture_request

    @abstractmethod
    def load(self) -> FixtureInstance:
        """Find and instantiate a fixture instance."""

    @abstractmethod
    def resolve_class_name(self) -> ClassVar:
        """Resolve fixture class to instantiate."""

    @abstractmethod
    def resolve_init_args(self) -> Dict[str, Any]:
        """Resolve init args for given fixture request."""


class InternalRemoteFixtureLoader(RemoteFixtureLoader):

    """
    Fixtures internally defined in the server.

    Notes
    -----
    1. Internal fixtures share the same process as the server.

    """

    def load(self) -> FixtureInstance:
        """Find and instantiate a fixture instance."""
        return InternalFixtureInstance(self.resolve_class_name(), self.resolve_init_args())

    def resolve_class_name(self) -> ClassVar:
        """Resolve fixture class to instantiate."""
        all_fixtures = api_lib.list_fixtures()
        for fixture in all_fixtures:
            if fixture["namespace"] != self.fixture_request.namespace:
                continue
            if fixture["name"] != self.fixture_request.name:
                continue
            # we have a match
            LOGGER.debug("Found internal fixture %s", fixture)
            return api_lib.get_fixture_class(self.fixture_request.namespace, self.fixture_request.name)
        raise RuntimeError(f"Unable to resolve fixture request: {self.fixture_request}")

    def resolve_init_args(self) -> Dict[str, Any]:
        """Resolve init args for given fixture request."""
        return {}
