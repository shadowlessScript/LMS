# Generated by Django 4.0.5 on 2023-03-24 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LIBSYS', '0061_rename_rating_rating_rate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='book',
            new_name='serial_number',
        ),
    ]
