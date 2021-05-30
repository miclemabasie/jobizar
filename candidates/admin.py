from django.contrib import admin
from .models import Skill, AppliedJob, SavedJob

admin.site.register(Skill)
admin.site.register(AppliedJob)
admin.site.register(SavedJob)
