from django.urls import path
from .views import (
    index, booking, appointment_create, appointment_update, appointment_delete,
    AppointmetListView, AppointmentDetailView,  OperationDetailView,
)
#AppointmentCreateView

urlpatterns = [
    path('home/', index, name='Index'),
    path('booking/', booking, name="Booking"),
    path('appointments-list/', AppointmetListView.as_view(), name="AppointmentsList"),
    path('appointment/make/operation-type/<int:oid>', appointment_create, name='AppointmentCreate'),
    path('appointment/<int:pk>/detail/', AppointmentDetailView.as_view(), name="AppointmentDetail" ),
    path('appointment/<int:pk>/update/', appointment_update ,name='AppointmentUpdate'),
    path('appointment/<int:pk>/delete/', appointment_delete, name='AppointmentDelete'),
    path('operation/<int:pk>/detail/', OperationDetailView.as_view(), name='OperationDetail'),
]