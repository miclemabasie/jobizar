from django.shortcuts import render, get_object_or_404, redirect, reverse
from users.models import Profile
from django.views.generic import ListView
from .models import Skill, AppliedJob, SavedJob
from recruiters.models import Job, Applicant, Selected
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.postgres.search import TrigramSimilarity

def search_job(request):
    query = request.GET.get('q')
    location = request.GET.get('p')

    object_list = []

    if query == None:
        object_list = Job.objects.all()
    else:
        # jobs_title = Job.objects.filter(title__icontains=query)
        jobs_title = Job.objects.annotate(similarity=TrigramSimilarity('title', query),).filter(similarity__gt=0.1)
        job_skills = Job.objects.annotate(similarity=TrigramSimilarity('skills_req', query),).filter(similarity__gt=0.1)
        job_type = Job.objects.annotate(similarity=TrigramSimilarity('job_type', query),).filter(similarity__gt=0.1)
        job_company = Job.objects.filter(company__name__icontains=query) 
        
        print("here are the list of jobs", jobs_title, job_skills, job_type, job_company)
        
        # job_skills = Job.objects.filter(skills_req__icontains=query)   
        # job_type = Job.objects.filter(job_type__icontains=query)

        for job in jobs_title:
            object_list.append(job)
            
        for job in job_skills:
            if job not in object_list:
                object_list.append(job)
        for job in job_company:
            if job not in object_list:
                object_list.append(job)

        for job in job_type:
            if job not in object_list:
                object_list.append(job)
        
        print(f"object list {object_list} ")

    if location == None:
        jobs_loc = Job.objects.all()
    else:
        jobs_loc = Job.objects.filter(location__icontains=location)

    final_job_list = []

    for i in object_list:
        if i in jobs_loc:
            final_job_list.append(i)
        
    final_job_list.reverse()
    page = request.GET.get('page')
    print(page)
    paginator = Paginator(final_job_list, 1)
    try:
        final_job_list = paginator.page(page)
    except PageNotAnInteger:
        final_job_list = paginator.page(1)
    except EmptyPage:
        final_job_list = paginator.page(1)

    context = {
        'jobs': final_job_list,
        'count': len(list(final_job_list)),
        'search': True,
        'page': page,
    }

    template_name = 'job-list.html'

    return render(request, template_name, context)

# class based view for job search
class SearchJobsListView(ListView):
    template_name = 'job-list.html'
    context_object_name = "jobs"
    paginate_by = 10
    def get_queryset(self, **kwargs):
        query = self.request.GET.get('q')
        location = self.request.GET.get('p')
        

        object_list = []

        if query == None:
            object_list = Job.activejobs.all()
        else:
            jobs_title = Job.objects.annotate(similarity=TrigramSimilarity('title', query),).filter(similarity__gt=0.1)
            job_skills = Job.objects.annotate(similarity=TrigramSimilarity('skills_req', query),).filter(similarity__gt=0.1)
            job_type = Job.objects.annotate(similarity=TrigramSimilarity('job_type', query),).filter(similarity__gt=0.1)
            job_company = Job.objects.filter(company__name__icontains=query) 
            print("here are the list of jobs", jobs_title, job_skills, job_type, job_company)

            for job in jobs_title:
                object_list.append(job)
                
            for job in job_skills:
                if job not in object_list:
                    object_list.append(job)
            for job in job_company:
                if job not in object_list:
                    object_list.append(job)

            for job in job_type:
                if job not in object_list:
                    object_list.append(job)

            print("here is the object list", object_list)

        if location == None:
            jobs_loc = Job.activejobs.all()
        else:
            jobs_loc = Job.activejobs.filter(location__icontains=location)

        final_job_list = []

        for i in object_list:
            if i in jobs_loc:
                final_job_list.append(i)
            
        final_job_list.reverse()

        # context = {
        #     'jobs': final_job_list,
        #     'count': len(list(final_job_list)),
        #     'search': True,
        #     'page': page,
        # }

        return final_job_list
    
    def get_context_data(self, **kwargs):
        try:
            js = self.kwargs['q']
        except:
            js = None
        context = super(SearchJobsListView, self).get_context_data(**kwargs)
        print(context)
        print(f"this are the kwargs {js}")
        return context
    

@login_required
def browse_jobs(request):
    jobs = Job.objects.all()
    user = request.user
    profiel = user.profile


    template_name = 'job-list.html'

    context = {
        'jobs': jobs
    }
    return render(request, template_name, context)

class BrowseJobs(ListView):
    template_name = 'job-list.html'
    queryset = Job.activejobs.all()
    context_object_name = 'jobs'
    paginate_by = 10

@login_required
def job_details(request, slug):
    job = get_object_or_404(Job, slug=slug)
    user = request.user
    profile = user.profile

    save_job_exists = SavedJob.objects.filter(user=user, job=job).exists()
    posted_by = job.recruiter.username

    if save_job_exists:
        saved = True
        print(saved)
    else:
        saved = False

    applied_job = AppliedJob.objects.filter(user=user, job=job).exists()

    if applied_job:
        applied = True
        print(applied)
    else:
        applied = False

    print(posted_by)

    template_name = 'job-details.html'
    context = {
        'job': job,
        'applied': applied,
        'saved': saved,
        'profile': profile,
        'posted_by': posted_by,
    }

    return render(request, template_name, context)

@login_required
def save_jobs(request, slug):
    job = get_object_or_404(Job, slug=slug)
    user = request.user

    save_job = SavedJob.objects.create(user=user, job=job)
    save_job.save()

    return redirect(f"/candidates/job-details/{slug}/")

def apply_job(request, slug):
    job = get_object_or_404(Job, slug=slug)
    user = request.user
    applied_job = AppliedJob.objects.create(user=user, job=job)
    applicant = Applicant.objects.create(applicant=user, job=job)
    applicant.save()
    applied_job.save()
    job.applied_count += 1
    job.save()
    return redirect(f"/candidates/job-details/{slug}/")
   


@login_required
def remove_jobs(request, slug):
    user = request.user
    remove_job = get_object_or_404(SavedJob, job__slug=slug)
    remove_job.delete()

    return redirect(f"/candidates/job-details/{slug}/")



def saved_jobs(request, slug):
    user = request.user
    profile = user.profile

    saved_jobs = SavedJob.objects.filter(user=user)

    template_name = 'candidates-saved-jobs.html'
    context = {
        'profile': profile,
        'jobs': saved_jobs
    }

    return render(request, template_name, context)


def intelligent_search(request):
    
    template_name = 'intelligent-search.html'
    context = {
        'jobs': 'jobs'
    }

    return render(request, template_name, context)