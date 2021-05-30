from django.urls import path
from .views import (
    search_job,
    browse_jobs,
    job_details,
    save_jobs,
    remove_jobs,
    apply_job,
    SearchJobsListView,
    BrowseJobs,
)


app_name = 'candidates'


urlpatterns = [
    path('job-search/',  search_job, name='job-search-list'),
    path('browse-jobs/', browse_jobs, name='browse-jobs'),
    path('job-details/<slug:slug>/', job_details, name='job-details'),
    path('save-job/<slug:slug>/', save_jobs, name='save-job'),
    path('remove-job/<slug:slug>/', remove_jobs, name='remove-job'),
    path('apply-job/<slug:slug>/', apply_job, name='apply-job'),
    path('job-searc-cbv/', SearchJobsListView.as_view(), name='cbv-search'),
    path('cbv-browse-all/', BrowseJobs.as_view(), name='cbv-browse-jobs')
]

