from django.db import models

# Create your models here.
FIXTURE_STATUS = [
    ("S", "Stable"),
    ("U", "Unstable"),
    ("d", "Deprecated"),
    ("D", "Deleted")
]


class TestSessionStatus(models.IntegerChoices):

    """Status for a test session."""

    CREATED = 1
    STARTING = 2
    STARTED = 3
    FINISHING = 4
    FINISHED = 5


class FixtureInstanceStatus(models.IntegerChoices):

    """Status for a test session."""

    CREATED = 1
    SETUP_RUNNING = 2
    SETUP_FINISHED = 3
    SETUP_FAILED = 4
    TEARDOWN_RUNNING = 5
    TEARDOWN_FINISHED = 6
    TEARDOWN_FAILED = 7


class FixtureDefs(models.Model):

    """Fixture model to capture a remote fixture."""

    class Meta:
        db_table = "cleanslate_fixture_defs"
        abstract = False

    namespace = models.CharField(max_length=100)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=1, choices=FIXTURE_STATUS)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class TestSession(models.Model):

    """A test session where all tests run."""

    class Meta:
        db_table = "cleanslate_test_session"
        abstract = False

    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)
    status = models.IntegerField(choices=TestSessionStatus.choices)
    exit_code = models.IntegerField(null=True)
    is_deleted = models.BooleanField(default=False)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)


class FixtureInstance(models.Model):

    """A running Fixture instance."""

    class Meta:
        db_table = "cleanslate_fixture_instances"
        abstract = False

    fixture_def_id = models.ForeignKey(FixtureDefs, on_delete=models.PROTECT)
    session_id = models.ForeignKey(TestSession, on_delete=models.PROTECT)
    status = models.IntegerField(choices=FixtureInstanceStatus.choices)
    message = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
