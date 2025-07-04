# Generated by Django 5.2.1 on 2025-06-24 11:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0004_remove_appointment_dental_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='operations_and_surgeries',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='appointment', to='clinic.operationsandsurgeries'),
        ),
    ]
