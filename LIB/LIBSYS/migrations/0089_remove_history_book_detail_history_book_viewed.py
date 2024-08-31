# Generated by Django 4.0.5 on 2023-08-16 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LIBSYS', '0088_remove_bookdetail_book_book_book_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='book_detail',
        ),
        migrations.AddField(
            model_name='history',
            name='book_viewed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='LIBSYS.book'),
        ),
    ]