# Generated by Django 3.1.2 on 2021-04-26 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
