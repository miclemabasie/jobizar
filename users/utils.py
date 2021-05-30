from django.utils.text import slugify
import random
import string

#Random strin gennerator
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#Random slug generator
def unique_slug_generator(instance, new_slug=None):
    if new_slug:
        slug = new_slug
    else:
        slug = slugify(instance.user.username)
    # get the class of the instance
    klass = instance.__class__

    # check if user exist inthe db with same slug
    qs_exist = klass.objects.filter(slug=slug).exists()

    if qs_exist:
        slug = slug 
        # create a random string
        random_str = random_string_generator(size=4)
        new_slug = f"{slug}-{random_slug}"
        return random_slug_generator(instance, new_slug=new_slug)

    return slug