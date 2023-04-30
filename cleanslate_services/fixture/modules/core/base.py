"""Base interfaces for implementing a fixture."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class FixtureException(Exception):

    """Exception raised while executing a fixture."""


class FixtureResult:

    """Serializable result returned by fixture setup."""

    def __init__(self, result: Optional[Any] = None, exc: Optional[FixtureException] = None):
        """
        Init fixture result.

        :param result: value returned by fixture.setup
        :param exc: exception occured during the execution of fixture

        """
        self.__exc = exc
        self.__result = result

    def is_exception(self) -> bool:
        """Return true if exception is set."""
        return self.__exc is not None

    def result(self) -> Any:
        """Return serialilzable result."""
        if not self.__result:
            raise self.__exc
        return self.__result

    def exc(self) -> Optional[FixtureException]:
        """Return fixture exception, else None."""
        return self.__exc


class RemoteFixtureImplBase(ABC):

    """Interface to define and implement a remote fixture."""

    def __init__(self):
        """Init a remote fixture instance."""

    @property
    def name(self):
        """Name of the remote fixture."""
        return self.__class__.name

    @abstractmethod
    def setup(self) -> FixtureResult:
        """Run setup logic for this fixture."""

    @abstractmethod
    def tear_down(self, setup_result: FixtureResult):
        """Run tear down with setup result."""
