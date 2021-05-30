from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from .models import Profile, Mail
from recruiters.models import Job
from .forms import UserUpdateForm, ProfileUpdateForm, SkillUpdateForm, MailingForm, ReportForm
from django.core.mail import send_mail
from django.contrib import messages


def mail_subcription(request, slug=None):
    p = request.GET.get('email')
       
    if request.user.is_authenticated:
        user = request.user
        qs_exists = Mail.objects.filter(user=user, email=p).exists()
        if qs_exists:
            messages.success(request, 'You already have a valid subcription')
            return redirect('/')
        else:
            mail = Mail.objects.create(user=user, email=p)
            profile = user.profile
            profile.subscriped = True
            profile.save()
            messages.success(request, "succesful subcription")
            return redirect('/')
    else:
        user =None
        qs_exists = Mail.objects.filter(email=p).exists()
        if qs_exists:
            messages.info('You already have a valid subcription')
            return redirect('/')
        else:
            mail = Mail.objects.create(user=user, email=p)
            return redirect('/')


def home(request):
    recent_jobs = Job.objects.all().order_by('-created_at')[:5]
    template_name = 'home.html'



    context = {
        'title': 'Home Page',
        'jobs': recent_jobs,
        
    }
    if request.user.is_authenticated:
        user = request.user
        profile = user.profile 
        
        try:
            company = profile.company
            if company:
                company = True
        except:
            company = False
        context['has_company'] = company

    return render(request, template_name, context)


@login_required
def policy(request):
    template_name = 'policy.html'
    user = request.user
    profile = user.profile
    profile.has_seen_policy = True
    profile.save()
    return render(request, template_name, {})


def recruiter_guide(request):
    template_name = 'recruiter-guide.html'

    return render(request, template_name, {})


@login_required
def ProfileView(request, slug):
    template_name = 'profile-view.html'
    profile = get_object_or_404(Profile, slug=slug)
    user = profile.user
    try:
        skills = user.skills.all().first().skill
        skills_list = skills.split(',')
        has_skills = True
    except:
        skills_list = None
        has_skills = False

    if request.user == user:
        edit = True
    else:
        edit = False
    
    context = {
        'profile': profile,
        'user': user,
        'edit': edit,
        'skills': skills_list,
        'has_skills': has_skills,
    }


    print(context['profile'])
    print(context['user'])

    return render(request, template_name, context)

@login_required
def update_profile(request, slug):
    user = request.user
    if request.method == 'POST':    
        user_form = UserUpdateForm(request.POST, instance=user)    
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        skill_form = SkillUpdateForm(request.POST, instance=user.skills.all().first())
        
        if user_form.is_valid() and profile_form.is_valid() and skill_form.is_valid():
            user_form.save()
            profile_form.save()
            skill = skill_form.save(commit=False)
            skill.user = request.user
            print(skill.user, skill)
            skill_form.save()
            

            send_mail(
                subject = 'Profile Updated',
                message = f"Dear {user.username} you have successfuly updated your profile",
                from_email = 'me@gmail.com',
                recipient_list = ['to@gmail.com', ]
            )
            print('done')
            
            return redirect(f"/users/profile/{slug}/")
        else:
            print('error')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=user.profile)
        skill_form = SkillUpdateForm(instance=user.skills.all().first())

    template_name = 'update-profile.html'
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'skill_form': skill_form,
    }

    return render(request, template_name, context)


def mailing_list(user):
    subject = 'New Job Post'
    message = f"Dear {user.name} a job was added you may want to take a look"
    from_email = 'metoyou@gmail.com'
    recip_list = [user.email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=(recip_list, ))


@login_required
def report_problem(request):
    if request.method == 'POST':
        form = ReportForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']

            subject = 'Report!'

            send_mail(subject=subject, message=message, from_email=email, recipient_list=('metoyou@gmail.com', ))
            print('done')
            return redirect('/')
        else:
            print('form not valid')
    elif request.method == 'GET':
        form = ReportForm()
    
    context = {
        'user': request.user,
        'form': form
    }

    template_name = 'report.html'

    return render(request, template_name, context)