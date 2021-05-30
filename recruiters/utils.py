import string
import random
from django.utils.text import slugify

# Random string generator
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def random_slug_generator(instance, new_slug = None):
    if new_slug:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    
    klass = instance.__class__

    instance_exist = klass.objects.filter(slug=slug).exists()

    if instance_exist:
        slug = slug
        # create a random string
        random_str = random_string_generator(size=4)
        new_slug = f"{slug}-{random_str}"
        return random_slug_generator(instance, new_slug=new_slug)

    return slug