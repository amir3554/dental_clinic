from django.http import HttpResponse
from django.shortcuts import render
from models import Slider, Appointment, OperationsAndSurgeries
from transaction.models import PaymentMethod
from django.views.generic import FormView
from dental_clinic_project import settings
from forms import AppointmentForm
from django.http.response import JsonResponse
from utils import make_transaction


def index(request):
    slides = Slider.objects.filter().all().order_by('order')
    return render(request ,'index.html', { 'slides' : slides })


def booking(request):
    oprations = OperationsAndSurgeries.objects.all()
    return render(request, 'booking/booking.html', { 'oprations' : oprations })


    




# stripe

def get_publishable_key(request):
    return JsonResponse(
        { 
            'publishable_key' : settings.STRIPE_PUBLISHABLE_KEY
        }
    )


def stripe_transaction(request):
    pass#transaction = make_transaction(request, PaymentMethod.STRIPE, )


