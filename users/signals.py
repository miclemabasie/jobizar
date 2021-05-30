from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from .utils import unique_slug_generator

@receiver(post_save, sender=User)
def create_user(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    

@receiver(post_save, sender=User)
def save_user(sender, instance, *args, **kwargs):
    instance.profile.save()



@receiver(pre_save, sender=Profile)
def create_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)