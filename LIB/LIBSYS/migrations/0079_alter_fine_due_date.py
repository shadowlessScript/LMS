# Generated by Django 4.0.5 on 2023-04-15 14:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LIBSYS', '0078_addbook_call_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fine',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 4, 15, 17, 39, 33, 225381)),
        ),
    ]