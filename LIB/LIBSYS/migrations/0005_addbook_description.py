# Generated by Django 4.0.3 on 2022-06-30 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LIBSYS', '0004_addbook_delete_addbookform'),
    ]

    operations = [
        migrations.AddField(
            model_name='addbook',
            name='description',
            field=models.TextField(default=' '),
        ),
    ]
