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

class OperationType(models.IntegerChoices):
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

    def __str__(self):
       return f"{self.name} ({self.get_job_display()})" #type:ignore


class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=5000, null=True)
    address = models.CharField(max_length=255)
    added_at = models.DateField(help_text="department opening date", null=True, blank=True)
    worker = models.ManyToManyField(Worker, related_name='department')
    email = models.EmailField(null=True, blank=True)
    contact = models.CharField(max_length=500, help_text="phone number , fax, etc...", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name



class Operation(models.Model):
    # this model will be filled by the admin
    # this way the user can chose the operation he wants with out manipulating anything
    dental_type = models.IntegerField(
        choices=OperationType.choices,
        default=OperationType.PERIODICAL_CHECKING,
    )
    description = models.TextField(max_length=5000, null=True, blank=True)
    price = models.FloatField()
    duration_minutes = models.IntegerField()
    image = models.ImageField(upload_to='operations_and_surgeries/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_worker(self):
        return self.role.worker #type:ignore

    def __str__(self) -> str:
        return f"{self.get_dental_type_display()}" #type:ignore


class Appointment(models.Model):
    operation = models.ForeignKey(
        Operation,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="appointment"
    )
    date = models.DateTimeField(null=False, blank=False)
    status = models.IntegerField(choices=AppointmentStatus.choices, default=AppointmentStatus.PENDING)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointment')
    department = models.ForeignKey(Department, on_delete=models.PROTECT,related_name='appointment')
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL,null=True, blank=True, related_name='appointment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        # Example to prevent the same patient from booking the same date twice
        unique_together = [['patient', 'date']]

    @property
    def get_price(self):
        return self.operation.price

    @property
    def get_dental_type(self):
        return self.operation.get_dental_type_display() #type:ignore
    

    @property
    def get_patient_username(self):
        return self.patient.username

    @property
    def get_department_name(self):
        return self.department.name

    @property
    def get_operation_time(self):
        return self.operation.duration_minutes

    @property
    def get_transaction_id(self):
        return self.transaction.id #type:ignore

    def __str__(self):
        date_str = self.date.strftime('%Y-%m-%d %H:%M') if self.date else 'unscheduled'
        return f"{self.patient.username} – {self.department.name} on {date_str} "



class Role(models.Model):
    worker = models.ForeignKey(
        Worker,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='role'
    )
    operation = models.ForeignKey(
        Operation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='role'
    )

    def __str__(self) -> str:
        return f'{self.operation} : {self.worker}'

    class Meta:
        unique_together = [['worker', 'operation']]


class Slider(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=1600)
    image = models.ImageField(upload_to='slider/', null=True, blank=True)
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title





