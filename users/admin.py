from django.contrib import admin
from .models import Profile, Mail

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'address']

admin.site.register(Mail)