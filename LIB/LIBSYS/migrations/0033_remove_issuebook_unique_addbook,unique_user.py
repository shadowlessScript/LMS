# Generated by Django 4.0.5 on 2023-02-23 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LIBSYS', '0032_alter_issuebook_serial_number_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='issuebook',
            name='unique_AddBook,unique_User',
        ),
    ]