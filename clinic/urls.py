from django.urls import path
from .views import (
    index, booking, get_publishable_key, appointment_create, appointment_update,
    AppointmentDetailView, 
)
#AppointmentCreateView

urlpatterns = [
    path('home/', index, name='Index'),
    path('booking/', booking, name="Booking"),
    path('appointment/make/operation-type/<int:oid>', appointment_create, name='AppointmentCreate'),
    path('appointment/<int:pk>/detail', AppointmentDetailView.as_view(), name="AppointmentDetail" ),
    path('appointment/<int:pk>/edit/', appointment_update ,name='AppointmentUpdate'),
    path('get-publishable-key/', get_publishable_key, name='get_publishable_key'),
    

]