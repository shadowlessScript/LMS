# Generated by Django 4.0.3 on 2022-05-26 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='signupForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('first_Name', models.CharField(max_length=50)),
                ('last_Name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=70)),
                ('password', models.CharField(max_length=100)),
                ('Confirmpass', models.CharField(max_length=100)),
            ],
        ),
    ]
