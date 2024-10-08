# Generated by Django 4.0.5 on 2023-08-14 15:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LIBSYS', '0084_alter_fine_due_date_alter_history_serial_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='serial_number',
        ),
        migrations.AddField(
            model_name='history',
            name='book_detail',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='LIBSYS.bookdetail'),
        ),
        migrations.AlterField(
            model_name='fine',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 8, 14, 18, 57, 26, 913050)),
        ),
    ]
