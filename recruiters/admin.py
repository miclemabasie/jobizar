from django.contrib import admin
from .models import Job, Applicant, Selected

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'company', 'recruiter', 'active']
    list_filter = ['created_at', 'updated_at']
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
    ordering = ('updated_at',)
    list_editable = ['active']

admin.site.register(Applicant)
admin.site.register(Selected)


    
    