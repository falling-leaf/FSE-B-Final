# Generated by Django 5.0.6 on 2024-06-06 13:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="deposit_record",
            fields=[
                (
                    "deposit_record_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("account_id", models.IntegerField()),
                ("deposit_type", models.CharField(max_length=10)),
                ("auto_renew_status", models.BooleanField()),
                ("deposit_start_date", models.DateField()),
                ("deposit_end_date", models.DateField()),
                ("deposit_amount", models.FloatField()),
                ("cashier_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="employee",
            fields=[
                ("employee_id", models.AutoField(primary_key=True, serialize=False)),
                ("employee_name", models.CharField(default="Unknown", max_length=20)),
                ("identity_card", models.CharField(default="Unknown", max_length=18)),
                ("employee_sex", models.IntegerField(default=0)),
                ("phone_number", models.CharField(default="Unknown", max_length=20)),
                ("occupation_name", models.CharField(default="Unknown", max_length=50)),
                ("is_employeed", models.BooleanField(default="False")),
                (
                    "other_information",
                    models.CharField(default="Unknown", max_length=1021),
                ),
            ],
        ),
        migrations.CreateModel(
            name="online_user",
            fields=[
                (
                    "user_id",
                    models.AutoField(default=0, primary_key=True, serialize=False),
                ),
                ("user_name", models.CharField(default="Unknown", max_length=20)),
                ("password", models.CharField(default="666666", max_length=20)),
                ("identity_card", models.CharField(max_length=18)),
                ("phone_num", models.CharField(default="10086", max_length=20)),
                ("is_frozen", models.BooleanField(default=False)),
                ("is_lost", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="transfer_record",
            fields=[
                (
                    "transfer_record_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("account_in_id", models.IntegerField()),
                ("account_out_id", models.IntegerField()),
                ("transfer_date", models.DateField()),
                ("transfer_amount", models.FloatField()),
                ("cashier_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="withdrawal_record",
            fields=[
                (
                    "withdrawal_record_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("account_id", models.IntegerField()),
                ("withdrawal_date", models.DateField()),
                ("withdrawal_amount", models.FloatField()),
                ("cashier_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="cashier",
            fields=[
                ("cashier_id", models.AutoField(primary_key=True, serialize=False)),
                ("account", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=20)),
                ("trade_authority", models.BooleanField()),
                ("manage_authority", models.BooleanField()),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bank_app.employee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="account",
            fields=[
                ("account_id", models.AutoField(primary_key=True, serialize=False)),
                ("password", models.CharField(max_length=20)),
                ("card_type", models.IntegerField()),
                ("balance", models.FloatField(default=0.0)),
                ("current_deposit", models.FloatField(default=0.0)),
                ("uncredited_deposit", models.FloatField(default=0.0)),
                ("is_frozen", models.BooleanField(default=False)),
                ("is_lost", models.BooleanField(default=True)),
                (
                    "identity_card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.SET_NULL,
                        to_field="identity_card",
                        db_column="identity_card",
                        to="bank_app.online_user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="sys_manage",
            fields=[
                ("sys_manager_id", models.AutoField(primary_key=True, serialize=False)),
                ("account", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=20)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bank_app.employee",
                    ),
                ),
            ],
        ),
    ]
