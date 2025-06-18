from django.db import models
from clinic.models import Appointment


class PaymentMethod(models.IntegerChoices):
    STRIPE = 1, "stripe"
    PAYPAL = 2, "paypal"

class TransactionStatus(models.IntegerChoices):
    DONE = 0, "done"
    PENDING = 1, 'pending'
    CANCELED = 2, 'canceled'



class Transaction(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    
    transaction_status = models.IntegerField(
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING
    )
    payment_method = models.IntegerField(choices=PaymentMethod.choices, null=True)

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE, related_name='transaction',
        help_text="For the payment related to this date"
    )

    transaction_id = models.CharField(
            max_length=100,
            unique=True,
            blank=True,
            null=True,
            help_text='Transaction number from payment gateway (webhook)'
        )

    session = models.CharField(max_length=255, null=True, blank=True)
    items = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.pk} - {self.appointment.patient.username} - {self.transaction_status}"

    @property
    def patient_name(self):
        return self.appointment.patient.username

    @property
    def patient_email(self):
        return self.appointment.patient.email
