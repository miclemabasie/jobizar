from django.db import models
from users.models import Profile


class Company(models.Model):
    name = models.CharField(max_length=255)
    line_of_engagement = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='companies', default="none.png", null=True, blank=True)
    about = models.TextField()
    link = models.CharField(max_length=1000, null=True, blank=True)
    mail = models.EmailField(null=True, blank=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    facebook = models.CharField(max_length=255, null=True, blank=True, help_text='Your facebook page link, Optional')
    google = models.CharField(max_length=255, null=True, blank=True, help_text='Your google plus page link, Optional')
    twitter = models.CharField(max_length=255, null=True, blank=True, help_text='Your twitter page link, Optional')
    linkedin = models.CharField(max_length=255, null=True, blank=True, help_text='Your linkedin page link, Optional')
    instagram = models.CharField(max_length=255, null=True, blank=True, help_text='Your facebook page link, Optional')
    slug = models.SlugField(unique=True, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save()
        self.name = str(self.name).upper()

    
    class Meta:
        verbose_name = 'companies'

    def __str__(self):
        return self.name
    
    