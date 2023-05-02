"""Refresh internal fixture definitions."""

import logging
import time

from django.core.management.base import BaseCommand

from fixture.modules.core.handlers import fixture, session

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):

    """Command to execute backend tasks for session and fixture execution."""

    help = "Updates all internal fixtures in the db."

    def handle(self, *args, **options):
        """Executes tasks and manages states for fixtures and sessions."""
        while True:
            handle_sessions()
            handle_fixtures()
            time.sleep(5)


def handle_sessions():
    """Handles sessions."""
    # newly created sessions must be set to STARTING
    session.session_created_to_starting()
    session.session_do_starting()

    # Finish sessions marked FINISHING
    session.session_do_finishing()

    # Mark sessions FINISHING if started time is past the lease duration
    session.session_lease_expired()

    # Set session FINISHED when all fixtures are terminated.
    session.session_finishing_to_finished()

def handle_fixtures():
    """Hanldes fixtures."""
    # Run setup for fixtures with status CREATED
    fixture.fixture_created_to_setup_pending()
    fixture.fixture_do_setup()

    # Set fixture state to TEARDOWN_PENDING for test sessions having state FINISHING
    fixture.fixture_setup_to_teardown_pending()

    # Run teardown for fixtures having state TEARDOWN_PENDING
    fixture.fixture_do_teardown()
