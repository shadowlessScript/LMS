# Generated by Django 4.0.5 on 2023-04-13 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LIBSYS', '0077_alter_bookreview_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='addbook',
            name='call_number',
            field=models.CharField(default='PR 6302 C6 R56', max_length=150),
        ),
    ]
