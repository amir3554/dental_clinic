from transaction.models import Transaction 
import stripe
import math
from forms import AppointmentForm
from django.http.response import JsonResponse



def make_transaction(pm, appointment, request, items):
    form = AppointmentForm(request.POST)
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