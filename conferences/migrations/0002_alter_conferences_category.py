# Generated by Django 5.1.1 on 2024-10-04 08:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('conferences', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conferences',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conferences', to='categories.category'),
        ),
    ]
