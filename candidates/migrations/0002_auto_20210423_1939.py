# Generated by Django 3.1.2 on 2021-04-23 19:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recruiters', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('candidates', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SaveJob',
            new_name='SavedJob',
        ),
    ]
