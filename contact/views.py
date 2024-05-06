from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

from .forms import ContactForm  # Assuming you have a form defined in forms.py

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Send email notification
            send_mail(
                f'Message from {name}',
                message,
                email,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            
        
            return render(request, 'contact/contact_success.html')
    else:
        form = ContactForm()
    
    return render(request, 'contact/contact.html', {'form': form})


def contact_success(request):
    return render(request, 'contact/contact_success.html')