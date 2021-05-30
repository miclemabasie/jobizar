from django.urls import path
from .views import (
    contact_form,
    contact_form_footer
)



app_name = 'contacts'

urlpatterns = [
    path('contact', contact_form, name='contact-form'),
    path('contact-footer', contact_form_footer, name='contact-footer')
]
