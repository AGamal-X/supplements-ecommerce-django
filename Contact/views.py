from django.contrib import messages
from django.shortcuts import redirect, render

from core.theme import template_path

from .models import Contact


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and message:
            Contact.objects.create(name=name, email=email, message=message)
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contact')
        messages.error(request, 'Please fill in all fields before sending your message.')
    return render(request, template_path('contact.html'))
