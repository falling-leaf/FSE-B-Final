# Generated by Django 5.0.6 on 2024-06-10 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit_record',
            name='deposit_update_date',
            field=models.DateField(null=True),
        ),
    ]