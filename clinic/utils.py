from transaction.models import Transaction 
from .forms import AppointmentEditForm
from django.http.response import JsonResponse
import stripe
import math


def make_transaction(pm, appointment, request, items):
    form = AppointmentEditForm(request.POST)
    if form.is_valid():
        try:
            amount = int(form.cleaned_data.get('amount', 0))
        except:
            return JsonResponse({ 'error' : 'while making a transaction' })

        return Transaction.objects.create(
                amount=math.ceil(amount),
                payment_method=pm,
                appointment = appointment,
                session=request.session.session_key,
                items=items,
            )


def make_appointment(request):
    pass 


# the user first opens the booking page
# then click on make appointment form to chose the dates and dental types
# when after submetting the form we make an appointment
# after this we make a transaction 
# after the transaction have been made , we initiate stripe session by JS and stripe form
# after submetting the form we make the transaction status = COMPLETED
# 



# path('fill-null/', views.fill_null),
# def fill_null(request):
#     from clinic.models import Appointment, OperationsAndSurgeries
#     default_op = OperationsAndSurgeries.objects.get(id=1) # for example
#     for appt in Appointment.objects.filter(operations_and_surgeries__isnull=True):
#         appt.operations_and_surgeries = default_op
#         appt.save()
#     return JsonResponse({'message' : 'Done' })


# path('fill-null-date/', views.fill_null_date),
# def fill_null_date(request):
#     from clinic.models import Appointment
#     from datetime import datetime
#     for appt in Appointment.objects.filter(date__isnull=True):
#         appt.date = datetime.now()
#         appt.save()
#     return JsonResponse({'message' : 'Done' })
