# Generated by Django 4.0.5 on 2023-08-07 07:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LIBSYS', '0080_book_library_alter_fine_due_date_bookdetail_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fine',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 8, 7, 10, 41, 13, 335711)),
        ),
    ]
