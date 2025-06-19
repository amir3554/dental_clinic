from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from forms import UserRegisterForm

class UserRegisterFormView(CreateView):
    form_class = UserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('LoginUser')
    




