"""Api implementation is here."""

import logging
from typing import Any, Dict, List, ClassVar

from fixture.data.test.fixtures import FirstFixture

LOGGER = logging.getLogger(__name__)


class FixtureRegistration:

    """Fixture registration."""

    def __init__(self):
        self.fixture_map: Dict[str, ClassVar] = {
            "test::a.b.c": FirstFixture
        }

    def list_all(self) -> List[str]:
        """List fixture namespace + keys."""
        return list(self.fixture_map.keys())


fixture_registration = FixtureRegistration()


def list_fixtures() -> List[Dict[str, Any]]:
    """List all available fixtures."""
    flist = fixture_registration.list_all()
    LOGGER.info("Found %d fixtures", len(flist))
    fixture_summary_list = []
    for fixture in flist:
        fixture_summary = {}
        name_parts = fixture.split("::")
        fixture_summary["namespace"] = name_parts[0]
        fixture_summary["name"] = name_parts[1]
        fixture_summary_list.append(fixture_summary)
    return fixture_summary_list


def get_fixture_class(namespace: str, name: str) -> ClassVar:
    """Get fixture class by namespace and name."""
    key = f"{namespace}::{name}"
    return fixture_registration.fixture_map[key]
