from django.db.models.signals import pre_save
from .models import Job
from django.dispatch import receiver
from .utils import random_slug_generator

@receiver(pre_save, sender=Job)
def create_job_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = random_slug_generator(instance)