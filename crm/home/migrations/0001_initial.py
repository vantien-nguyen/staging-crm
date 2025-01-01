# Generated by Django 5.1.4 on 2025-01-01 00:51

import django.contrib.postgres.fields
import django.db.models.deletion
import home.models.account
import home.models.partner
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(null=True)),
                (
                    "siren",
                    models.CharField(
                        max_length=9,
                        unique=True,
                        validators=[home.models.account.validate_siren],
                    ),
                ),
                (
                    "code_postal",
                    models.CharField(
                        max_length=5,
                        validators=[home.models.account.validate_code_postal],
                    ),
                ),
                (
                    "turnover",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=15
                    ),
                ),
                (
                    "cash",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=15
                    ),
                ),
                ("website", models.URLField(blank=True, null=True)),
                ("typology", models.CharField(max_length=255)),
                (
                    "polymorphic_ctype",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="polymorphic_%(app_label)s.%(class)s_set+",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "db_table": "accounts",
            },
        ),
        migrations.CreateModel(
            name="Billing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("billing_date", models.DateTimeField(auto_created=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("reason", models.TextField()),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=15
                    ),
                ),
            ],
            options={
                "db_table": "billings",
            },
        ),
        migrations.CreateModel(
            name="File",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(max_length=128)),
                ("url", models.URLField(blank=True, null=True)),
                ("size", models.PositiveIntegerField()),
                ("mime_type", models.CharField(blank=True, max_length=64, null=True)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Uploading", "Uploading"),
                            ("Success", "Success"),
                            ("Failed", "Failed"),
                        ],
                        default="Uploading",
                        max_length=20,
                    ),
                ),
            ],
            options={
                "db_table": "files",
            },
        ),
        migrations.CreateModel(
            name="Kyc",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Completed", "Completed"),
                            ("Canceled", "Canceled"),
                        ],
                        default="Pending",
                        max_length=20,
                    ),
                ),
                ("notes", models.TextField(null=True)),
                ("der", models.BooleanField(default=False)),
                ("qcf", models.BooleanField(default=False)),
            ],
            options={
                "db_table": "kycs",
            },
        ),
        migrations.CreateModel(
            name="Opportunity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_date", models.DateTimeField(auto_created=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "nominal",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=15
                    ),
                ),
                (
                    "margin",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=15
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Interest", "Interest"),
                            ("Agreed-Client", "Agreed-Client"),
                            ("Agreed-Partner", "Agreed-Partner"),
                            ("Successful", "Successful"),
                            ("Unsuccessful", "Unsuccessful"),
                        ],
                        default="Interest",
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "transfer_type",
                    models.CharField(
                        choices=[("One-Time", "One-Time"), ("Recurring", "Recurring")],
                        default="Recurring",
                        max_length=20,
                    ),
                ),
                (
                    "frequency",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Monthly", "Monthly"),
                            ("Quarterly", "Quarterly"),
                            ("Annually", "Annually"),
                        ],
                        default="Monthly",
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=15
                    ),
                ),
                (
                    "maturity",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=10
                    ),
                ),
                ("sous_jacent", models.CharField(max_length=64, null=True)),
                ("coupon_payments", models.CharField(max_length=64, null=True)),
                (
                    "rates",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=10
                    ),
                ),
                (
                    "traab",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=10
                    ),
                ),
                (
                    "capital_protection",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=15
                    ),
                ),
                (
                    "coupon_protection",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=15
                    ),
                ),
                ("start_date", models.DateTimeField(null=True)),
                ("end_date", models.DateTimeField(null=True)),
            ],
            options={
                "db_table": "opportunities",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(null=True)),
                ("typology", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "db_table": "products",
            },
        ),
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "account_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="home.account",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("Client", "Client"), ("Prospect", "Prospect")],
                        default="Client",
                        max_length=20,
                    ),
                ),
                (
                    "needs",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=1000, null=True),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "existing_partners",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=1000, null=True),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
            ],
            options={
                "db_table": "clients",
            },
            bases=("home.account",),
        ),
        migrations.CreateModel(
            name="Partner",
            fields=[
                (
                    "account_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="home.account",
                    ),
                ),
                (
                    "iban",
                    models.CharField(
                        blank=True,
                        max_length=34,
                        null=True,
                        validators=[home.models.partner.validate_iban],
                    ),
                ),
                (
                    "bic",
                    models.CharField(
                        blank=True,
                        max_length=34,
                        null=True,
                        validators=[home.models.partner.validate_bic],
                    ),
                ),
            ],
            options={
                "db_table": "partners",
            },
            bases=("home.account",),
        ),
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                ("email", models.EmailField(max_length=254, null=True)),
                ("linkedin", models.URLField(blank=True, null=True)),
                ("job_description", models.TextField(null=True)),
                (
                    "account",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contacts",
                        to="home.account",
                    ),
                ),
                (
                    "file",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contact",
                        to="home.file",
                    ),
                ),
            ],
            options={
                "db_table": "contacts",
            },
        ),
        migrations.AddField(
            model_name="account",
            name="file",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="account",
                to="home.file",
            ),
        ),
        migrations.CreateModel(
            name="Interaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("date_time", models.DateTimeField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Planed", "Planed"),
                            ("Done", "Done"),
                            ("Canceled", "Canceled"),
                        ],
                        default="Planed",
                        max_length=20,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("Call", "Call"),
                            ("Mail", "Mail"),
                            ("Appointment", "Appointment"),
                            ("Visual", "Visual"),
                        ],
                        default="Call",
                        max_length=20,
                    ),
                ),
                ("comment", models.TextField(null=True)),
                (
                    "contact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interactions",
                        to="home.contact",
                    ),
                ),
            ],
            options={
                "db_table": "interactions",
            },
        ),
    ]