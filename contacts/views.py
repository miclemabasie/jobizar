from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from django.core.mail import send_mail


@login_required
def contact_form(request):
    user = request.user
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            subject = form.cleaned_data.get('subject')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            recip_list = 'joberdesk@gmail.com'
            send_mail(subject=subject, message=message, from_email=email, recipient_list=(recip_list, ))
            return redirect('/')
        else:
            print(form.errors)
    else:
        form = ContactForm()

    template_name = 'contact-form.html'
    context = {
        'form': form,
    }

    return render(request, template_name, context)


def contact_form_footer(request):
    name = request.GET.get('name')
    email = request.GET.get('email')
    message = request.GET.get('message')

    print(request.GET)
    
    if name and email and message:
        subject = 'Email From Footer'
        recip_list = 'joberdesk@gmail.com'
        send_mail(subject=subject, message=message, from_email=email, recipient_list=(recip_list,))
        return redirect('/')
    else:
        print('errors')
        return redirect('/')

        