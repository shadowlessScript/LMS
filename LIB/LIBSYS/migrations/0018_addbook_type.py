# Generated by Django 4.0.5 on 2022-09-21 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LIBSYS', '0017_borrowbook_clients_name_fine'),
    ]

    operations = [
        migrations.AddField(
            model_name='addbook',
            name='type',
            field=models.CharField(choices=[('online', 'online'), ('physical', 'physical'), ('physical/online', 'physical/online')], default='online', max_length=20),
        ),
    ]