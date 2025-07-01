from django.db.models.query import QuerySet
from django.db.models import Prefetch  
from django.forms import ModelForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView
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
from .models import Slider, Appointment, Operation, Patient, Department, Worker, Role
from .forms import  AppointmentModelForm
from datetime import datetime
import json
import random
from typing import Any




def index(request):
    slides = Slider.objects.filter().all().order_by('order')
    department = Department.objects.filter().all()
    return render(request ,'index.html', { 'slides' : slides, 'department' : department })


def booking(request):
    operations = Operation.objects.all().prefetch_related(
        Prefetch(
            'role',
            queryset=Role.objects.select_related('worker')
            )
        )
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


class AppointmetListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'booking/appointments_list.html'
    context_object_name = 'appointments'   #{% for appt in appointments %}

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user.pk).select_related('operation')



class AppointmentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Appointment
    template_name = 'booking/detail.html'
    context_object_name = 'appointment'


    def test_func(self) -> bool:
        return (self.request.user == self.get_object().patient)  #type:ignore


class OperationDetailView(DetailView):
    model = Operation
    template_name = 'booking/operation.html'
    context_object_name = 'operation'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        workers = Worker.objects.filter(role__operation=self.object).prefetch_related(     #type:ignore
            Prefetch(
                'role',
                queryset=Role.objects.filter(operation=self.object), #type:ignore
                to_attr='filtered_roles'  
                )
            ).prefetch_related('department')
        context['workers'] = workers
        return context
    



@login_required
@require_http_methods(['GET', 'POST'])
def appointment_create(request, oid : int) -> HttpResponse:

    patient = Patient.objects.get(pk=request.user.id)
    operation = get_object_or_404(Operation, id=oid)
    workers = Worker.objects.filter(role__operation=operation.pk)
    departments = Department.objects.filter(worker__in=workers).distinct()

    if request.method == "POST":
        form = AppointmentModelForm(request.POST,allowed_workers=workers, allowed_departments=departments)
        if form.is_valid():    
            try:
                date_str = request.POST.get('date')
                date_str_format = datetime.strptime(date_str, "%d-%m-%Y %I:%M%p")
            except:
                return render(request, 'booking/create.html',{'form': form,'date_error' : 'DateTime picker error try again.'})
            
            worker = form.cleaned_data.get('worker') or random.choice(workers)
            department = form.cleaned_data.get('department')

            if worker not in workers:
                form.add_error('worker', 'This agent is not authorized to perform the operation.')
            elif department not in departments:
                form.add_error('department', 'wrong department')

            if form.errors:
                return render(request, 'booking/create.html', {'form': form})

            appointment = Appointment.objects.create(
                operation = operation,
                patient = patient,
                department = department,
                worker = worker,
                date = date_str_format
            )
            appointment.save()
            return redirect(reverse('AppointmentDetail', kwargs={'pk' : appointment.pk}))
    
    form = AppointmentModelForm(allowed_workers=workers, allowed_departments=departments)
    return render(request, 'booking/create.html', {'form' : form})


@login_required
@require_http_methods(['GET', 'POST'])
def appointment_update(request, pk):

    appointment = get_object_or_404(Appointment, pk=pk)
    workers = Worker.objects.filter(role__operation=appointment.operation.pk)
    departments = Department.objects.filter(worker__in=workers)

    if request.user != appointment.patient:
        return HttpResponseForbidden()

    if request.method == "POST":
        form = AppointmentModelForm(request.POST,allowed_workers=workers, allowed_departments=departments)
        if form.is_valid():
            worker = form.cleaned_data.get('worker') or random.choice(workers)
            department = form.cleaned_data['department']

            if worker not in workers:
                form.add_error('worker', 'This agent is not authorized to perform the operation.')
            elif department not in departments:
                form.add_error('department', 'wrong department')
            
            if form.errors:
                return render(request, 'booking/create.html', {'form': form})

            appointment.worker = worker
            appointment.department = department
            appointment.save()
            return redirect('AppointmentDetail', pk)
        
    form = AppointmentModelForm(
        allowed_workers=workers,
        allowed_departments=departments
    )
    return render(
        request,
        'booking/update.html',
        {
            'form' : form ,
            'appointment' : appointment,
        }
    )


@login_required
@require_http_methods(['POST'])
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    
    if appointment.patient != request.user:
        return HttpResponseForbidden()
    
    appointment.delete()
    return redirect('AppointmentsList')


# the reverse filteration if we have the worker
# this will be add when we add the (about us) page, which has the workers info.
#allowed_operations = Operation.objects.filter(role__worker=worker)
