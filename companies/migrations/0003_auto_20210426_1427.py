# Generated by Django 3.1.2 on 2021-04-26 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_auto_20210426_1353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='image',
            new_name='logo',
        ),
    ]
