from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import redirect, render

# Create your views here.
from .forms import CustomUserCreationForm

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'
