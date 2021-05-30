import random
import string
from django.utils.text import slugify


# Generationg a random string
def generate_random_string(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Generate a random unique slug for the campany
def unique_slug_generator(instance, new_slug=None):
    if new_slug:
        slug = new_slug
    else:
        slug = slugify(instance.name)
    
    klass = instance.__class__

    qs_exists = klass.objects.filter(slug=slug).exists()

    if qs_exists:
        slug = slug
        random_str = generate_random_string(size=4)
        new_slug = f"{slug}-{random_str}"
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug