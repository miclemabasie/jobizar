from django.urls import path

from .views import (
    add_job,
    job_recruiter_detail,
    get_all_recruiter_jobs,
    update_job,
    job_detail_table,
    select_applicant,
    remove_job,
    company_job_analytics,
)

app_name = 'recruiters'

urlpatterns = [
    path('add-job/', add_job, name='add-job'),
    path('recruiter-job-detail/<slug:slug>/', job_recruiter_detail, name='recruiter-job-detail'),
    path('update-job/<slug:slug>/', update_job, name='update-job'),
    path('job-rec-detail/<slug:slug>/', job_detail_table, name='job-detail-table'),
    path('all-recruiter-jobs/<slug:slug>/', get_all_recruiter_jobs, name='all-recruiter-jobs'),
    path('select-applicant/<slug:job>/<slug:user>/', select_applicant, name='select-applicant'),
    path('romove-job/<slug:slug>/', remove_job, name='remove-job'),
    path('company-jobs-analytics/<slug:slug>/', company_job_analytics, name='company-jobs-analytics')
]
