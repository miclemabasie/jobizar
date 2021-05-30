from django import forms
from .models import Job

class AddJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'location', 'job_type', 'skills_req', 'link', 'intro', 'description', 'min_salary', 'max_salary']

class UpdateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'location', 'skills_req', 'link', 'intro', 'description', 'min_salary', 'max_salary']