# Generated by Django 3.1.2 on 2021-05-03 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiters', '0018_auto_20210502_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='applied_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='selected_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
