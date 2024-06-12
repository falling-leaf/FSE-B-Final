# Generated by Django 5.0.6 on 2024-06-11 02:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bank_app", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="identity_card",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="accounts",
                to="bank_app.online_user",
            ),
        ),
    ]
