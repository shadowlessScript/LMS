# Generated by Django 4.0.5 on 2022-09-22 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LIBSYS', '0021_alter_addbook_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addbook',
            name='genre',
            field=models.CharField(choices=[('Engineering', (('Civil Engineering', 'Civil Engineering'), ('Software Engineering', 'Software Engineering'), ('Computer Science', 'Computer Science'))), ('Economics', ((' Classical economics', ' Classical economics'), ('Neo-classical economics', 'Neo-classical economics'))), ('Novel', 'Novel'), ('Science', 'Science'), ('Business', 'Business'), ('Mathematics', 'Mathematics')], default='Engineering', max_length=50),
        ),
    ]