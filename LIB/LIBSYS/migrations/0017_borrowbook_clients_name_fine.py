# Generated by Django 4.0.5 on 2022-09-21 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LIBSYS', '0016_alter_addbook_cover_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowbook',
            name='clients_name',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Fine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(blank=True, null=True)),
                ('clients_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='LIBSYS.borrowbook')),
            ],
        ),
    ]