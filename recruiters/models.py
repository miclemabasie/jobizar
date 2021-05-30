from django.db import models
from django.contrib.auth.models import User
from companies.models import Company
from ckeditor.fields import RichTextField



JOB_TYPES = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Internship', 'Internship'),
    ('Remote', 'Remote'),
    ('Contract', 'Contract')
)

class JobActiveManage(models.Manager):
    def get_queryset(self):
        return super(JobActiveManage, self).get_queryset().filter(active=True)
    

class Job(models.Model):
    recruiter = models.ForeignKey(User, related_name='jobs', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    intro = models.TextField(null=True, help_text="Enter a brief description of the job post")
    description = models.TextField()
    job_type = models.CharField(choices=JOB_TYPES, max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=250)
    skills_req = models.CharField(max_length=250)
    image = models.ImageField(upload_to='job_pics/', default='job.jpeg', null=True, blank=True)
    max_applicants = models.PositiveIntegerField(null=True, blank=True)
    link = models.CharField(max_length=1024, null=True, blank=True, help_text='Provide a link to your site if only you wish the applicants to apply on your site')
    active = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, null=True, blank=True)
    min_salary = models.IntegerField(null=True, blank=True)
    max_salary = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    applied_count = models.IntegerField(default=0, null=True, blank=True)
    selected_count = models.IntegerField(default=0, null=True, blank=True)
    objects = models.Manager()
    activejobs = JobActiveManage()
    

    def __str__(self):
        return str(self.title)

class Applicant(models.Model):
    job = models.ForeignKey(Job, related_name='applied_jobs', on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, related_name='job_applicant', on_delete=models.CASCADE)
    date_applied = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return str(self.applicant.username)
    

class Selected(models.Model):
    job = models.ForeignKey(Job, related_name='selected_jobs', on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, related_name='selected_applicants', on_delete=models.CASCADE)
    date_selected = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.applicant.username)