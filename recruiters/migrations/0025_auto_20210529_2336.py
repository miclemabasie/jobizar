# Generated by Django 3.1.2 on 2021-05-29 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiters', '0024_job_intro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='image',
            field=models.ImageField(blank=True, default='job.jpeg', null=True, upload_to='job_pics/'),
        ),
        migrations.AlterField(
            model_name='job',
            name='intro',
            field=models.TextField(blank=True, help_text='Enter a brief description of the job post', null=True),
        ),
    ]
