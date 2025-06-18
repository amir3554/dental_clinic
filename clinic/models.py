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
    description = models.TextField(max_length=5000, null=True)
    date = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(max_length=4)
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


