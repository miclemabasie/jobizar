# Generated by Django 3.1.2 on 2021-05-03 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_profile_subscriped'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='has_job',
            field=models.BooleanField(default=False),
        ),
    ]
