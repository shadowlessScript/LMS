# Generated by Django 4.0.5 on 2022-09-13 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LIBSYS', '0008_alter_new_story'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]