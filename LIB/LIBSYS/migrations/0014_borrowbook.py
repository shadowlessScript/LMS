# Generated by Django 4.0.5 on 2022-09-16 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LIBSYS', '0013_delete_signupform'),
    ]

    operations = [
        migrations.CreateModel(
            name='BorrowBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_borrowed', models.DateField(auto_now_add=True)),
                ('name_of_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LIBSYS.addbook')),
            ],
        ),
    ]