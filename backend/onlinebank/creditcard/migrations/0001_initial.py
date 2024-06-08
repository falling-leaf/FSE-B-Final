# Generated by Django 5.0.6 on 2024-06-06 11:56

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.AutoField(primary_key=True, serialize=False)),
                ('employee_name', models.CharField(default='name', max_length=20)),
                ('identity_card', models.CharField(default='000000000000000000', max_length=18)),
            ],
        ),
        migrations.CreateModel(
            name='Online_user',
            fields=[
                ('person_id', models.AutoField(primary_key=True, serialize=False)),
                ('identity_card', models.CharField(default='000000000000000000', max_length=18)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transfer_record_id', models.AutoField(primary_key=True, serialize=False)),
                ('account_in_id', models.IntegerField()),
                ('account_out_id', models.IntegerField()),
                ('transfer_amount', models.IntegerField()),
                ('transfer_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='CreditCardExaminer',
            fields=[
                ('credit_examiner_id', models.AutoField(primary_key=True, serialize=False)),
                ('check_authority', models.BooleanField(default=False)),
                ('account', models.CharField(default='000000', max_length=30)),
                ('password', models.CharField(default='password', max_length=20)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='creditcard.employee')),
            ],
        ),
        migrations.CreateModel(
            name='CreditCardApplication',
            fields=[
                ('apply_id', models.AutoField(primary_key=True, serialize=False)),
                ('apply_status', models.BooleanField(default=False)),
                ('apply_result', models.BooleanField(default=False)),
                ('apply_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('have_open', models.BooleanField(default=False)),
                ('creditCardExaminer', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='creditcard.creditcardexaminer')),
                ('online_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='creditcard.online_user')),
            ],
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('account_id', models.AutoField(primary_key=True, serialize=False)),
                ('password', models.CharField(default='password', max_length=20)),
                ('card_type', models.CharField(default='credit', max_length=10)),
                ('credit_limit', models.FloatField(default=1000.0)),
                ('balance', models.FloatField(default=0.0)),
                ('is_frozen', models.BooleanField(default=False)),
                ('is_lost', models.BooleanField(default=False)),
                ('open_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('online_user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='creditcard.online_user')),
            ],
        ),
    ]
