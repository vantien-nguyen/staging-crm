# Generated by Django 5.1.4 on 2025-01-01 13:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="billing",
            name="file",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="billing",
                to="home.file",
            ),
        ),
    ]
