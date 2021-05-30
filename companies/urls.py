from django.urls import path
from .views import (
    setup_company,
    company_home_page,
    company_profile_view,
    update_company_profile,
)
app_name = 'companies'

urlpatterns = [
    path('setup-company-profile/<slug:slug>/', setup_company, name='setup-company'),
    path('update-company-profile/<slug:slug>/', update_company_profile, name='update-company-profile'),
    path('company-home-page/<slug:slug>/', company_home_page, name='company-home-page'),
    path('company-profile-view/<slug:slug>/', company_profile_view, name='company-profile-view')
]
