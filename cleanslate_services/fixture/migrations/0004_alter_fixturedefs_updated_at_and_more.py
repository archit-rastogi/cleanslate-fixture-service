# Generated by Django 4.2 on 2023-04-22 09:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fixture", "0003_alter_fixtureinstance_message"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fixturedefs",
            name="updated_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="fixtureinstance",
            name="updated_at",
            field=models.DateTimeField(null=True),
        ),
    ]
