import uuid

from django.db import models

# Create your models here.
FIXTURE_STATUS = [
    ("S", "Stable"),
    ("U", "Unstable"),
    ("d", "Deprecated"),
    ("D", "Deleted")
]


class SessionStatus(models.IntegerChoices):

    """Status for a test session."""

    CREATED = 1
    STARTING = 2
    STARTED = 3
    FINISHING = 4
    FINISHED = 5
    ERROR = 6


class FixtureInstanceStatus(models.IntegerChoices):

    """Status for a test session."""

    CREATED = 1
    SETUP_PENDING = 2
    SETUP_RUNNING = 3
    SETUP_FINISHED = 4
    SETUP_FAILED = 5
    TEARDOWN_PENDING = 6
    TEARDOWN_RUNNING = 7
    TEARDOWN_FINISHED = 8
    TEARDOWN_FAILED = 9


class FixtureType(models.IntegerChoices):

    """Types of fixtures."""

    FIXTURE_INTERNAL = 1
    FIXTURE_GITHUB = 2
    FIXTURE_DOCKER = 3


class ResourceType(models.IntegerChoices):

    """Types of Resources."""

    JSON_RESOURCE = 1


class FixtureDefs(models.Model):

    """Fixture model to capture a remote fixture."""

    class Meta:
        db_table = "cleanslate_fixture_defs"
        abstract = False
        unique_together = ["namespace", "name"]

    namespace = models.CharField(max_length=100)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=1, choices=FIXTURE_STATUS)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)
    fixture_type = models.IntegerField(choices=FixtureType.choices, default=None, null=True)


class Session(models.Model):

    """A session is where all fixtures run."""

    class Meta:
        db_table = "cleanslate_session"
        abstract = False

    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)
    status = models.IntegerField(choices=SessionStatus.choices)
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

    fixture_def_id = models.ForeignKey(FixtureDefs, null=True, on_delete=models.PROTECT)
    session_id = models.ForeignKey(Session, on_delete=models.PROTECT)
    status = models.IntegerField(choices=FixtureInstanceStatus.choices)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)


class ResourceContent(models.Model):

    """Content of a resource."""

    class Meta:
        db_table = "cleanslate_resource_content"
        abstract = False

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = models.BinaryField(null=True, editable=False, max_length=4096)


class Resource(models.Model):

    """A resource instance."""

    class Meta:
        db_table = "cleanslate_resource"
        abstract = False

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resource_type = models.IntegerField(choices=ResourceType.choices)
    content = models.ForeignKey(ResourceContent, null=True, on_delete=models.PROTECT)
