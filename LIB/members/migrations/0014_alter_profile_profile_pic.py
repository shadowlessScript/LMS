# Generated by Django 4.0.5 on 2023-04-08 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0013_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='images/profile_pic/22/default.jpg', null=True, upload_to='images/profile_pic/%y'),
        ),
    ]
