# Generated by Django 4.0.5 on 2023-02-22 09:04

import LIBSYS.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LIBSYS', '0025_issuebook'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuebook',
            name='expirydate',
            field=models.DateField(default=LIBSYS.models.expiry),
        ),
    ]