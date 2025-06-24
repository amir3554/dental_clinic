from django.urls import path, include
from django.contrib.auth.views import LoginView
from .forms import UserLoginForm
from .views import UserRegisterFormView

urlpatterns = [
    path('login/',  LoginView.as_view(authentication_form=UserLoginForm), name='login'),
    path('register/',  UserRegisterFormView.as_view(), name='Register'),
    path('', include('django.contrib.auth.urls')),
]
