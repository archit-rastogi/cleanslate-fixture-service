# Generated by Django 4.2 on 2023-05-02 13:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fixture", "0006_rename_testsession_session_alter_resource_content_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fixtureinstance",
            name="status",
            field=models.IntegerField(
                choices=[
                    (1, "Created"),
                    (2, "Setup Pending"),
                    (3, "Setup Running"),
                    (4, "Setup Finished"),
                    (5, "Setup Failed"),
                    (6, "Teardown Pending"),
                    (7, "Teardown Running"),
                    (8, "Teardown Finished"),
                    (9, "Teardown Failed"),
                ]
            ),
        ),
    ]