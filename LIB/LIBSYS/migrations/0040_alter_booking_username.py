# Generated by Django 4.0.5 on 2023-02-26 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LIBSYS', '0039_alter_returnedbook_return_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
