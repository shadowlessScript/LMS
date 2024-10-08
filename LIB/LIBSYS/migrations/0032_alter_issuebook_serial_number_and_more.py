# Generated by Django 4.0.5 on 2023-02-23 09:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LIBSYS', '0031_alter_booking_serial_number_alter_booking_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuebook',
            name='serial_number',
            field=models.ForeignKey(db_constraint=False, db_index=False, on_delete=django.db.models.deletion.CASCADE, to='LIBSYS.addbook'),
        ),
        migrations.AlterField(
            model_name='issuebook',
            name='username',
            field=models.ForeignKey(db_constraint=False, db_index=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='issuebook',
            constraint=models.UniqueConstraint(fields=('username', 'serial_number'), name='unique_AddBook,unique_User'),
        ),
    ]
