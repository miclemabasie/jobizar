from django.urls import path
from .views import(
    home,
    ProfileView,
    update_profile,
    policy,
    recruiter_guide,
    mail_subcription,
    report_problem,
)

app_name = 'users'

urlpatterns = [
    path('', home, name='home'),
    path('users/profile/<slug:slug>/', ProfileView, name='profile-view' ),
    path('users/profile-update/<slug:slug>/', update_profile, name='profile-update'),
    path('policy/', policy, name='policy'),
    path('guide/', recruiter_guide, name='recruiter-guide'),
    path('subcribe-to-mailinglist/', mail_subcription, name='mailing-subscription'),
    path('report/', report_problem, name='report')
]
