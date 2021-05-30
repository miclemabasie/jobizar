from django.shortcuts import render, get_object_or_404, redirect
from recruiters.models import Job, Selected, Applicant
from .models import Company
from django.contrib.auth.decorators import login_required
from .forms import CreateCompanyForm, UpdateCompanyProfileForm
from users.models import Profile
from django.core.mail import send_mail
from django.contrib import messages




@login_required
def setup_company(request, slug):
    user = request.user
    profile = get_object_or_404(Profile, slug=slug)
    try:
        jobs = Job.objects.filter(recruiter=user)
    except:
        jobs = None

    if request.method == 'POST':
        form = CreateCompanyForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.profile = profile
            form.save()
            for job in jobs:
                job.company = profile.company
                job.save()
            profile.has_company = True
            profile.save()
            subject = 'Company Created'
            message = 'You just created you created a company account at JobLister Thanks for your loyalty'
            from_email = 'metoyou@gmail.com'
            email_list = ['you@gmail.com',]
            send_mail(subject, message, from_email, email_list)
            
            return redirect('/')                                          
        else:
            return form.errors
    elif request.method == 'GET':
        form = CreateCompanyForm()
    
    template_name = 'setup-company.html'

    context = {
        'profile': profile,
        'form': form,
        'user': user,
        'recruiter': True,
    }

    return render(request, template_name, context)

@login_required()   
def update_company_profile(request, slug):
    company = get_object_or_404(Company, slug=slug)
    user = company.profile.user
    if request.method == 'POST':
        if user == request.user:
            form = UpdateCompanyProfileForm(request.POST or None, request.FILES, instance=company)
            if form.is_valid():
                form.save()
                messages.success(request, 'successfully updated your company profile info')
                return redirect(f"/companies/company-profile-view/{slug}/")
            else:
                print(form.errors)
        else:
            print('Not Eligible')
            return redirect('/')
    else:
        form = UpdateCompanyProfileForm(instance=company)
    
    template_name = 'update-company-profile.html'
    context = {
        'form': form,
        'company': company,
        'recruiter': True,
    }
    return render(request, template_name, context)

    
@login_required
def company_home_page(request, slug):
    user = request.user
    profile = user.profile
    company = get_object_or_404(Company, slug=slug)
    template_name = 'company-home-page.html'
    jobs = Job.objects.filter(company=company)
    context = {
        'title': 'home page',
        'company': company,
        'jobs': jobs,
        'recruiter': True,
    }

    return render(request, template_name, context)



@login_required
def company_profile_view(request, slug):
    company = get_object_or_404(Company, slug=slug)
    template_name = 'company-profile-view.html'
    user = company.profile.user
    if request.user == user:
        rec = True
        edit = True
    else:
        rec = False
        edit = False
    context = {
        'company': company,
        'recruiter': rec,
        'edit': edit,
    }

    return render(request, template_name, context)