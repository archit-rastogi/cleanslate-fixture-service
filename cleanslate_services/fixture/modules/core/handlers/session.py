"""Handlers for session execution."""


def session_created_to_starting():
    """
    Transition a session from CREATED to STARTING.

    Notes
    -----
    1. Allocate a runtime or compute env to the session.
    2. Set state for session to STARTING or ERROR.

    """


def session_do_starting():
    """
    Transition session from STARTING to STARTED.

    Notes
    -----
    1. Complete any setup required to host and run fixtures.
    2. Set state for session to STARTED or ERROR.

    """


def session_do_finishing():
    """All fixtures are marked TEARDOWN_PENDING."""


def session_lease_expired():
    """Mark sessions which are past their leased duration to FINISHING."""


def session_finishing_to_finished():
    """Session having no active fixtures are marked FINISHED."""
