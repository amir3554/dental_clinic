from django import forms
from .models import Appointment

attrs = { 'class' : 'form-control' }

class AppointmentModelForm(forms.ModelForm):


    class Meta:

        model = Appointment

        fields = ['worker', 'department']

        labels = {
            'department' : 'Department',
            'worker' : 'Worker'
        }

        widgets = {
            #'date' : forms.DateTimeInput(attrs=attrs, format='%Y-%m-%dT%H:%M'),
            'department' : forms.Select(attrs=attrs),
            'worker' : forms.Select(attrs=attrs)
        }



# class AppointmentEditForm(forms.ModelForm):

#     class Meta:

#         model = Appointment

#         fields = ['department', 'worker']

#         labels = {
#             'department' : 'Department',
#             'worker' : 'Worker'
#         }

#         widgets = {
#             #'date' : forms.DateTimeInput(attrs={ 'class' : '' }, format='%Y-%m-%dT%H:%M'),
#             'department' : forms.Select(attrs=attrs),
#             'worker' : forms.Select(attrs=attrs)
#         }
       

