# Generated by Django 4.0.5 on 2022-09-23 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LIBSYS', '0022_alter_addbook_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='addbook',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='books/%y'),
        ),
    ]