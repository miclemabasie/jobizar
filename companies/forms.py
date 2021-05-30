from django import forms
from .models import Company


class CreateCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['name', 'location', 'about', 'logo']


class UpdateCompanyProfileForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'location', 'about', 'logo', 'facebook', 'google', 'twitter', 'linkedin', 'instagram']