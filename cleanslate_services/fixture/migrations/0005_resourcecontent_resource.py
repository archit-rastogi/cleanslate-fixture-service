# Generated by Django 4.2 on 2023-04-28 19:50

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("fixture", "0004_alter_fixturedefs_updated_at_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ResourceContent",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("data", models.BinaryField(max_length=4096, null=True)),
            ],
            options={
                "db_table": "cleanslate_resource_content",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Resource",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("resource_type", models.IntegerField(choices=[(1, "Json Resource")])),
                (
                    "content",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fixture.resourcecontent",
                    ),
                ),
            ],
            options={
                "db_table": "cleanslate_resource",
                "abstract": False,
            },
        ),
    ]