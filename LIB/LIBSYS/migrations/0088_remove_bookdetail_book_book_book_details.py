# Generated by Django 4.0.5 on 2023-08-16 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LIBSYS', '0087_remove_issuebook_book_issued'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookdetail',
            name='book',
        ),
        migrations.AddField(
            model_name='book',
            name='book_details',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='LIBSYS.bookdetail'),
        ),
    ]
