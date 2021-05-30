from django.dispatch import  receiver
from django.db.models.signals import pre_save
from .models import Company
from .utils import  unique_slug_generator


@receiver(pre_save, sender=Company)
def add_slug(sender, instance, *args, **kwargs):
    print(instance)
    if not instance.slug:
        print(instance)
        instance.slug = unique_slug_generator(instance)