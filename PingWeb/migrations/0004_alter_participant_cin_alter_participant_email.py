# Generated by Django 5.1.1 on 2024-10-11 08:42

import PingWeb.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PingWeb', '0003_alter_participant_options_alter_reservation_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='cin',
            field=models.CharField(max_length=8, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(message='this field must contain exactly 8 digits', regex='^\\d{8}$')]),
        ),
        migrations.AlterField(
            model_name='participant',
            name='email',
            field=models.EmailField(max_length=255, unique=True, validators=[PingWeb.models.email_validator]),
        ),
    ]
