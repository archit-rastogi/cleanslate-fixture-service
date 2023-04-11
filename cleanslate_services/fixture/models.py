from django.db import models

# Create your models here.
FIXTURE_STATUS = [
    ("S", "Stable"),
    ("U", "Unstable"),
    ("d", "Deprecated"),
    ("D", "Deleted")
]


class Fixture(models.Model):

    """Fixture model to capture a remote fixture."""

    class Meta:
        db_table = "cleanslate_fixture"
        abstract = False

    namespace = models.CharField(max_length=100)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=1, choices=FIXTURE_STATUS)
