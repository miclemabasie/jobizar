# Generated by Django 3.1.2 on 2021-04-23 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiters', '0004_job_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
