from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile_pics/', default='profile_pic/profile.png')
    proffession = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    looking_for = models.CharField(max_length=100)
    works_at = models.CharField(max_length=200, null=True, blank=True, help_text='Tell us where you currently work (optional)')
    bio = models.TextField()
    date_of_birth = models.DateTimeField(null=True)
    instagram = models.CharField(max_length=200, null=True, blank=True, help_text='Provide link to your instagram account (optional)')
    google_plus = models.CharField(max_length=200, null=True, blank=True, help_text='Provide link to your Google Plus account (optional)')
    facebook = models.CharField(max_length=200, null=True, blank=True, help_text='Provide link to your Facebook account (optional)')
    twitter = models.CharField(max_length=200, null=True, blank=True, help_text='Provide link to your Twitter account (optional)')
    linked_in = models.CharField(max_length=200, null=True, blank=True, help_text='Provide link to your Linked In account (optional)')
    has_seen_policy = models.BooleanField(default=False, null=True, blank=True)
    has_company = models.BooleanField(default=False)
    has_job = models.BooleanField(default=False)
    subscriped = models.BooleanField(default=False)
    resume = models.FileField(upload_to="users-resume")
    

    def __str__(self):
        return f"{str(self.user.username)} profile"


class Mail(models.Model):
    user = models.ForeignKey(User, related_name='mails', on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()

    def __str__(self):
        return f"{self.email}"