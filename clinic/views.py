from django.forms import ModelForm
from django.views.generic import CreateView, FormView, DetailView, UpdateView
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, HttpResponseForbidden
from django.http.response import JsonResponse
from django.shortcuts import render, redirect,  get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from transaction.models import PaymentMethod
from dental_clinic_project import settings
from .models import Slider, Appointment, OperationsAndSurgeries, Patient, Department
from .forms import  AppointmentModelForm
from .utils import make_transaction
from datetime import datetime


import json


def index(request):
    slides = Slider.objects.filter().all().order_by('order')
    department = Department.objects.filter().all()
    return render(request ,'index.html', { 'slides' : slides, 'department' : department })


def booking(request):
    operations = OperationsAndSurgeries.objects.all()
    paginator = Paginator(operations, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'booking/booking.html',
        {
            'page_obj' : page_obj,
        }
    )

# class AppointmentCreateView(LoginRequiredMixin, CreateView):
#     model = Appointment
#     form_class = AppointmentModelForm
#     template_name = 'booking/create.html'

#     def form_valid(self, form: ModelForm) -> HttpResponse:
#         self.object = form.save()
#         return super().form_valid(form)

#     def get_success_url(self) -> str:
#         return reverse('AppointmentDetail', args=self.get_object().pk)
@login_required
@require_http_methods(['GET', 'POST'])
def appointment_create(request, oid : int) -> HttpResponse:
    if request.method == "POST":
        form = AppointmentModelForm(request.POST)
        if form.is_valid():
            try:
                date_str = request.POST.get('date')
                date_str_format = datetime.strptime(date_str, "%d-%m-%Y %I:%M%p")
            except Exception as e:
                return JsonResponse(
                    {
                        'status': 'error',
                        'message' : 'DateTime picker error make sure you have chosen the date before the time'
                    },
                    status=400
                )
            operation_type = OperationsAndSurgeries.objects.get(pk=oid)
            patient = Patient.objects.get(pk=request.user.id)
            form_data = form.cleaned_data
            appointment = Appointment.objects.create(
                operations_and_surgeries = operation_type,
                patient = patient,
                department = form_data.get('department'),
                worker = form_data.get('worker'),
                date = date_str_format
            )
            return redirect('AppointmentDetail', appointment.pk)
    form = AppointmentModelForm()
    return render(request, 'booking/create.html', { 'form' : form })


@login_required
@require_http_methods(['GET', 'POST'])
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.user != appointment.patient:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = AppointmentModelForm(request.POST)
        try:
            date_str = request.POST.get('date')
            date_str_format = datetime.strptime(date_str, '%d-%m-%y %I:%M%p')
        except Exception as e:
                return JsonResponse(
                    {
                        'status': 'error',
                        'message' : 'DateTime picker error make sure you have chosen the date before the time'
                    },
                    status=400
                )
        appointment.date = date_str_format
        appointment.worker = form.cleaned_data.get('worker')
        appointment.department = form.cleaned_data.get('department') #type:ignore
        appointment.save()
        return redirect('AppointmentDetail', pk)
    form = AppointmentModelForm()
    return render(request, 'booking/update.html', { 'form' : form })






class AppointmentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Appointment
    template_name = 'booking/detail.html'

    def test_func(self) -> bool:
        return (self.request.user == self.get_object().patient)  #type:ignore



# stripe

def get_publishable_key(request):
    return JsonResponse(
        { 
            'publishable_key' : settings.STRIPE_PUBLISHABLE_KEY
        }
    )


def stripe_transaction(request):
    pass#transaction = make_transaction(request, PaymentMethod.STRIPE, )


