import logging
import time

from fixture.modules.core.base import FixtureResult, RemoteFixtureImplBase

LOGGER = logging.getLogger(__name__)


class FirstFixture(RemoteFixtureImplBase):

    """Fixture implementation."""

    def setup(self):
        """Setup implementation."""
        LOGGER.info("Setup invoked!")
        LOGGER.info("Will sleep for 10 seconds while pretending to do something!")
        time.sleep(10)
        LOGGER.info("Setup will exit now!")
        return FixtureResult(result={"value": 4, "sleep_duration": 10})

    def tear_down(self, setup_result: FixtureResult):
        """Teardown for first fixture."""
        LOGGER.info("Teardown invoked!")
        time_to_sleep = 5
        if setup_result is not None:
            LOGGER.info("setup result is: %s", setup_result.result)
            time_to_sleep = setup_result.result["sleep_duration"]
        LOGGER.info("Will slepp for %d s and pretend to teardown!", time_to_sleep)
        time.sleep(time_to_sleep)
        LOGGER.info("Teardown will exit now!")
