# Generated by Django 3.1.2 on 2021-05-02 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiters', '0015_auto_20210501_0839'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='applied_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
