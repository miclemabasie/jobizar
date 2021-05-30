from django.shortcuts import reverse
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published')
)

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    body = RichTextField()
    # body = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to='post-pics')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = TaggableManager()
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', args=[self.publish.year,
                                                self.publish.month,
                                                self.publish.day,
                                                self.slug,])
                                                

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f"{self.name} comment on {self.post.title}"
    