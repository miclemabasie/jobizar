from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Applicant, Selected
from django.contrib.auth.decorators import login_required
from .forms import AddJobForm, UpdateJobForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from users.views import mailing_list
from users.models import Mail, Profile


@login_required
def add_job(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = AddJobForm(request.POST or None, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.recruiter = request.user
            print(profile)
            try:
                form.company = request.user.profile.company
                has_company = True
            except:
                form.company = None
                has_company = False
                
            form.save()

            if not has_company:
                subject = 'Job posted'
                message = f'Dear {user.username} you just posted a job "{form.title}" but you do not have a company account we strongly recomment that you get one going!.'
                send_mail(subject, 
                        message,
                        from_email='metoyou@gmail.com',recipient_list=['you@gmail.com',])
            
            mail_list = Mail.objects.all()
            if mail_list:
                for i in mail_list:
                    subject = 'New Job Post'
                    message = f"Dear {i.user.username} a Job was added at joberdesk"
                    from_email = 'metoyou@gmail.com'
                    recip_list = i.email
                    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=(recip_list,))

            if not user.profile.has_job:
                profile.has_job = True
                profile.save()
                print('profile not has job')
            else:
                print('profile hase job')
            return redirect('/')
    else:
        form = AddJobForm()

    template_name = 'add-job.html'
    context = {
        'form': form,
        'profile': profile,
        'recruiter': True,
    }

    return render(request, template_name, context)

@login_required
def update_job(request, slug):
    user = request.user
    job = get_object_or_404(Job, slug=slug)
    
    if job.recruiter == user:
        job = job
    else:
        job = None
        return redirect('/')
    if request.method == 'POST':
        form = UpdateJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            print('saved')
            return redirect('/')
        else:
            print('error')
            return form.errors

    else:
        form = UpdateJobForm(instance=job)
    
    context = {
        'job': job,
        'form': form,
        'recruiter': True,
    }

    template_name = 'update-job.html'
    return render(request, template_name, context)


    
@login_required
def job_recruiter_detail(request, slug):
    user = request.user
    job = get_object_or_404(Job, slug=slug, recruiter=user)
    
    applicant_count = job.applied_jobs.all().count()
    selected_applicant_count = job.selected_jobs.all().count()
    template_name = 'recruiter-job-detail.html'

    context = {
        'job': job,
        'applicant_count': applicant_count,
        'selected_applicant_count': selected_applicant_count,
        'recruiter': True,
    }
    print(context['job'])

    return render(request, template_name, context)

@login_required
def remove_job(request, slug):
    user = request.user
    job = get_object_or_404(Job, slug=slug)
    if request.method == 'POST':
        job.delete()
        if user.profile.has_company:
            company = user.profile.company
            return redirect(f"/companies/company-home-page/{company.slug}/")
        else:
            return redirect(f"/recruiters/all-recruiter-jobs/{request.user.profile.slug}/")
    
    template_name = 'recruiter-delete-job.html'
    context ={
        'job': job,
        'recruiter': True,
    }
    return render(request, template_name, context)

@login_required
def get_all_recruiter_jobs(request, slug):
    user = request.user
    profile = user.profile

    jobs = Job.objects.filter(recruiter=user)

    template_name = 'recruiter-jobs.html'
    context = {
        'jobs': jobs,
        'recruiter': True,
    }

    return render(request, template_name, context)


def job_detail_table(request, slug):
    job = get_object_or_404(Job, slug=slug)
    recruiter = job.recruiter
    
    try:
        company = recruiter.profile.company
    except:
        company = None
    
    if company:
        pass

    applicants = Applicant.objects.filter(job=job)
    selected_applicants = Selected.objects.filter(job=job)

    selected_candidates_count = Selected.objects.filter(job=job).count()
    applied_candidates_count = Applicant.objects.filter(job=job).count()

    selected_list = []

    for i in selected_applicants:
        selected_list.append(i.applicant.username)
    
    print(selected_list)
    template_name = 'job-table-detail.html'
    context = {
        'job': job,
        'company': company,
        'applicant_list': applicants,
        'selected_list': selected_list,
        'selected_count': selected_candidates_count,
        'applied_count': applied_candidates_count,
        'recruiter': True,
    }

    print(applicants)

    return render(request, template_name, context)


def select_applicant(request, job, user):
    job = get_object_or_404(Job, slug=job)
    user = get_object_or_404(User, username=user)
    job.selected_count += 1 
    selected_applicant = Selected.objects.create(job=job, applicant=user)
    selected_applicant.save()
    job.save()

    subject = 'Selected Candidate'
    message = f"Dear {user.username} you've been selected for interview concerning a job post you applied for at jobdesk.com please visit link to get in touch with the recruiter as fast as posible"
    from_email = 'metoyou@gmail.com'
    recip_list = [user.email]

    send_mail(subject=subject, message=message,from_email=from_email, recipient_list=recip_list )
    
    return redirect(f"/recruiters/job-rec-detail/{job.slug}/")



@login_required
def company_job_analytics(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    user = profile.user
    try:
        jobs = Job.objects.filter(recruiter=user)
    except:
        jobs = None

    context = {
        'jobs': jobs,
        'recruiter': True,
    }

    template_name = 'company-job-analytics.html'
    
    return render(request, template_name, context)
