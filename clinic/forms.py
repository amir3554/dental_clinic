from django import forms
from .models import Appointment

attrs = { 'class' : 'form-control' }

class AppointmentModelForm(forms.ModelForm):


    class Meta:

        model = Appointment

        fields = ['worker', 'department']

        labels = {
            'department' : 'Department',
            'worker' : 'The Operator'
        }

        widgets = {
            #'date' : forms.DateTimeInput(attrs=attrs, format='%Y-%m-%dT%H:%M'),
            'department' : forms.Select(attrs=attrs),
            'worker' : forms.Select(attrs=attrs)
        }


    def __init__(self, *args, allowed_workers=None, allowed_departments=None, **kwargs):
        super().__init__(*args, **kwargs)
        if allowed_workers is not None:
            self.fields['worker'].queryset = allowed_workers #type:ignore
        if allowed_departments is not None:
            self.fields['department'].queryset = allowed_departments #type:ignore



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
       

