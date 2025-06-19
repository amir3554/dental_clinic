from django.urls import path
from django.contrib.auth.views import LoginView
from forms import UserLoginForm
from views import UserRegisterFormView

urlpatterns = [
    path('login/',  LoginView.as_view(authentication_form=UserLoginForm), name='UserLogin'),
    path('register/',  UserRegisterFormView.as_view(authentication_form=UserLoginForm), name='UserRegister'),
]
