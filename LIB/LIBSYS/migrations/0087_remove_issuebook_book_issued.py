# Generated by Django 4.0.5 on 2023-08-16 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LIBSYS', '0086_rename_new_announcement_remove_issuebook_isbn_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issuebook',
            name='book_issued',
        ),
    ]