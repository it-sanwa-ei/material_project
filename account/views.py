from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.shortcuts import redirect, render
from django.forms import ValidationError
# Create your views here.
from .forms import CustomUserCreationForm
from django.contrib import messages

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        dept_code = form.cleaned_data['dept_code']
        if dept_code == 'pkYwfygDTV':
            temp_form = super(RegisterView, self).form_valid(form=form)
            form.instance.department = 'Managerial'
            form.save()
            return temp_form
        elif dept_code == 'gNdcKFPMXT':
            temp_form = super(RegisterView, self).form_valid(form=form)
            form.instance.department = 'Accounting & Finance'
            form.save()
            return temp_form
        elif dept_code == 'JNTpmYmpqn':
            temp_form = super(RegisterView, self).form_valid(form=form)
            form.instance.department = 'HRD & GA'
            form.save()
            return temp_form
        elif dept_code == 'sYJZGxIxZL':
            temp_form = super(RegisterView, self).form_valid(form=form)
            form.instance.department = 'Warehouse'
            form.save()
            return temp_form
        elif dept_code == 'xtgopPPThR':
            temp_form = super(RegisterView, self).form_valid(form=form)
            form.instance.department = 'Quality'
            form.save()
            return temp_form
        elif dept_code == 'oNScatdztu':
            temp_form = super(RegisterView, self).form_valid(form=form)
            form.instance.department = 'ICT'
            form.save()
            return temp_form
        elif dept_code == 'BcWoNinSMs':
            temp_form = super(RegisterView, self).form_valid(form=form)
            form.instance.department = 'Mold Maintenance'
            form.save()
            return temp_form
        elif dept_code == 'rwiXIaxDWS':
            temp_form = super(RegisterView, self).form_valid(form=form)
            form.instance.department = 'Maintenance'
            form.save()
            return temp_form
        elif dept_code == 'KTADPeqjKi':
            temp_form = super(RegisterView, self).form_valid(form=form)
            form.instance.department = 'Production'
            form.save()
            return temp_form
        elif dept_code == 'iYWiZHFATU':
            temp_form = super(RegisterView, self).form_valid(form=form)
            form.instance.department = 'Tool Room & Mold Shop'
            form.save()
            return temp_form
        else:
            return HttpResponse("<script>alert('Invalid Department Code.'); history.back();</script>")
            


class LoginAdminView(TemplateView):
    template_name= 'registration/login_admin.html'