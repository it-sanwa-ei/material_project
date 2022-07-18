from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
# Create your views here.

from .forms import ContactUsForm

class GuestHomeTemplateView(TemplateView):
    template_name='guest/guest_home.html'

class AboutUsTemplateView(TemplateView):
    template_name='guest/guest_about_us.html'

class CompanyStructureTemplateView(TemplateView):
    template_name='guest/guest_company_structure.html'

class ProductsTemplateView(TemplateView):
    template_name='guest/guest_products.html'

class InjectionMoldingTemplateView(TemplateView):
    template_name='guest/guest_injection_molding.html'

class MoldMakingTemplateView(TemplateView):
    template_name='guest/guest_mold_making.html'

class MoldMaintenanceTemplateView(TemplateView):
    template_name='guest/guest_mold_maintenance.html'

class QualityControlTemplateView(TemplateView):
    template_name='guest/guest_quality_control.html'

class CareerTemplateView(TemplateView):
    template_name='guest/guest_career.html'

class ContactUsTemplateView(FormView):
    form_class = ContactUsForm
    template_name='guest/guest_contact_us.html'

def guest_send_email(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            guest_name = form.cleaned_data['guest_name']
            guest_email = form.cleaned_data['guest_email']
            guest_subject = form.cleaned_data['guest_subject']
            guest_message = form.cleaned_data['guest_message']
            guest_attachment = form.cleaned_data['guest_attachment']

            try:
                mail = EmailMessage(subject=str(guest_subject) + ' - ' + str(guest_name), body=guest_message + '\n\nRedirected from ' + str(guest_email), from_email=guest_email, to=['pga@sanwa-ei.com'],)
                print(mail)
                if guest_attachment:
                    mail.attach(guest_attachment.name, guest_attachment.read(), guest_attachment.content_type)
                mail.send()
            except Exception as e:
                return HttpResponse("<script> alert( '%s' );history.back();</script>"%(e))
            return HttpResponseRedirect(reverse('guest_email_success'))
        else:
            return HttpResponse('<script> alert("Make sure all fields are entered and valid.");history.back();</script>')
    else:
        reverse_lazy('guest_contact_us')

class GuestSendMailSuccessTemplateView(TemplateView):
    template_name = 'guest/guest_send_mail_success.html'