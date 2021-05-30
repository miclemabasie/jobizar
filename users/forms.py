from django import forms
from .models import Profile, Mail
from django.contrib.auth.models import User
from candidates.models import Skill


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'address', 'phone', 'proffession', 'looking_for', 'image', 'bio', 'date_of_birth', 'instagram', 'google_plus', 'facebook', 'twitter', 'linked_in', 'resume']

class SkillUpdateForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill']

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mail
        fields = ['email']


class ReportForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)