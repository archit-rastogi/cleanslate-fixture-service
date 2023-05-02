"""Handlers for fixture execution and state management."""

def fixture_created_to_setup_pending():
    """Fixture created should transition to SETUP_PENDING when session is STARTED."""


def fixture_do_setup():
    """Setup is executed and transitions to SETUP_FINISHED or SETUP_FAILED."""


def fixture_setup_to_teardown_pending():
    """All fixtures transition to TEARDOWN_PENDING when a fixture status is SETUP_FAILED."""


def fixture_do_teardown():
    """Teardown is executed and transitions to TEARDOWN_FINISHED or TEARDOWN_FAILED."""
