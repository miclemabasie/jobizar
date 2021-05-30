from django.db import models
from django.contrib.auth.models import User
from recruiters.models import Job
from django.utils import timezone

class Skill(models.Model):
    user = models.ForeignKey(User, related_name='skills', on_delete=models.CASCADE)
    skill = models.CharField(max_length=250)


class AppliedJob(models.Model):
    user = models.ForeignKey(User, related_name='applied_user', on_delete=models.CASCADE)
    job = models.ForeignKey(Job, related_name='applied_job', on_delete=models.CASCADE)
    date_applied = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.job.title)
    

class SavedJob(models.Model):
    user = models.ForeignKey(User, related_name='saved', on_delete=models.CASCADE)
    job = models.ForeignKey(Job, related_name='saved_jobs', on_delete=models.CASCADE)
    date_saved = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.job.title)