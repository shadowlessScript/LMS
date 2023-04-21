# Generated by Django 4.0.5 on 2023-03-27 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LIBSYS', '0063_fine_status_alter_fine_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='addbook',
            name='co_authors',
            field=models.CharField(blank=True, max_length=240, null=True),
        ),
        migrations.AddField(
            model_name='addbook',
            name='edition',
            field=models.CharField(default='first edition', max_length=50),
        ),
        migrations.AddField(
            model_name='addbook',
            name='pages',
            field=models.IntegerField(default=150),
        ),
        migrations.AddField(
            model_name='addbook',
            name='publisher',
            field=models.CharField(default='Nami printers', max_length=150),
        ),
    ]