# Generated by Django 4.0.5 on 2023-02-22 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LIBSYS', '0028_issuebook_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='addbook',
            name='copies',
            field=models.IntegerField(default=1),
        ),
    ]
