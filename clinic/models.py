from django.db import models
from patient.models import Patient


class Job(models.IntegerChoices):
    SECRETARY = 1, 'secretary'
    NURSE = 2, 'nurse'
    TECHNICIAN = 3, 'technician'
    DOCTOR = 4, 'doctor'
    WORKER = 5, 'worker'
    OTHER = 6, 'other'
    ADMIN = 7, 'admin'


class AppointmentStatus(models.IntegerChoices):
    DONE = 0, "done"
    PENDING = 1, 'pending'
    CANCELED = 2, 'canceled'

class OperationsAndSurgeriesTypes(models.IntegerChoices):
    # Preventative and Restorative
    DENTAL_CLEANING = 1, "Dental Cleaning (Prophylaxis)"
    DENTAL_FILLING = 2, "Dental Filling (Restoration)"
    ROOT_CANAL = 3, "Root Canal Therapy (Endodontics)"

    # Surgical
    TOOTH_EXTRACTION = 4, "Tooth Extraction"
    DENTAL_IMPLANT = 5, "Dental Implant Placement"

    # Cosmetic/Specialized
    TEETH_WHITENING = 6, "Teeth Whitening"
    ORTHODONTIC_TREATMENT = 7, "Orthodontic Treatment"

    # check appontment
    PERIODICAL_CHECKING = 8, 'Periodical Checking'

class Worker(models.Model):
    name = models.CharField(max_length=64)
    job = models.IntegerField(choices=Job.choices, default=Job.OTHER)
    salary = models.FloatField()

    #def __str__(self):
    #    return f"{self.name} ({self.get_job_display()})"


class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=5000, null=True)
    address = models.CharField(max_length=255)
    added_at = models.DateField(help_text="department opening date", null=True, blank=True)
    worker = models.ManyToManyField(Worker, related_name='department')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Appointment(models.Model):
    dental_type = models.IntegerField(choices=OperationsAndSurgeriesTypes.choices,null=True,blank=True)
    date = models.DateTimeField(null=True, blank=True)
    appointment_status = models.IntegerField(choices=AppointmentStatus.choices, default=AppointmentStatus.PENDING)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointment')
    department = models.ForeignKey(Department, on_delete=models.PROTECT,related_name='appointments')
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL,null=True, blank=True, related_name='appointments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        # مثال لمنع حجز نفس المريض لنفس التاريخ مرتين
        unique_together = [['patient', 'date']]

    def __str__(self):
        return f"{self.patient.username} – {self.department.name} on {self.date:%Y-%m-%d %H:%M}" #type:ignore



class Slider(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=1600)
    image = models.ImageField(upload_to='slider', null=True, blank=True)
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OperationsAndSurgeries(models.Model):
    # this model will be filled by the admin
    # this way the user can chose the operation he wants with out manipulating anything
    price = models.FloatField()
    description = models.TextField(max_length=5000, null=True, blank=True)
    duration_minutes = models.IntegerField(max_length=4)
    dental_type = models.IntegerField(
        choices=OperationsAndSurgeriesTypes.choices,
        default=OperationsAndSurgeriesTypes.PERIODICAL_CHECKING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



"""

Okay, here are 7 common types of dental operations and surgeries, suitable for your Django project's models.IntegerChoices and with short descriptions for a web project. I'll include the Python code for the IntegerChoices class and then the descriptions.

Python

from django.db import models

class OperationAndSurgeryType(models.IntegerChoices):
    # Preventative and Restorative
    DENTAL_CLEANING = 1, "Dental Cleaning (Prophylaxis)"
    DENTAL_FILLING = 2, "Dental Filling (Restoration)"
    ROOT_CANAL = 3, "Root Canal Therapy (Endodontics)"

    # Surgical
    TOOTH_EXTRACTION = 4, "Tooth Extraction"
    DENTAL_IMPLANT = 5, "Dental Implant Placement"

    # Cosmetic/Specialized
    TEETH_WHITENING = 6, "Teeth Whitening"
    ORTHODONTIC_TREATMENT = 7, "Orthodontic Treatment"
Descriptions for Your Web Project:
Here are the 7 types of operations and their short descriptions for your web content:

Dental Cleaning (Prophylaxis)

Description: A routine preventative procedure to remove plaque, tartar, and surface stains from your teeth, crucial for maintaining optimal oral hygiene and preventing cavities and gum disease.
Dental Filling (Restoration)

Description: Used to restore a tooth damaged by decay back to its normal function and shape. The decayed portion is removed, and the space is filled with a durable material like composite resin or amalgam.
Root Canal Therapy (Endodontics)

Description: A procedure to treat infection or damage deep inside a tooth. The infected pulp is removed, the inner chamber is cleaned and disinfected, and then filled and sealed to save the natural tooth.
Tooth Extraction

Description: The removal of a tooth from its socket in the bone. This may be necessary due to severe decay, infection, overcrowding, or damage beyond repair.
Dental Implant Placement

Description: A surgical procedure to replace missing tooth roots with titanium screw-like posts. These implants fuse with your jawbone, providing a strong foundation for artificial teeth (crowns, bridges, or dentures).
Teeth Whitening

Description: A popular cosmetic procedure designed to lighten the natural color of your teeth, effectively removing stains and discoloration to achieve a brighter, more radiant smile.
Orthodontic Treatment

Description: Involves the use of braces, clear aligners, or other appliances to correct misaligned teeth and jaws, improving bite function, oral health, and the aesthetics of your smile.
"""