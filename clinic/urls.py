from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.index, name='Index'),
    path('get-publishable-key/', views.get_publishable_key, name='get_publishable_key')



]