# Generated by Django 4.0.5 on 2022-09-20 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
