from django.db import models


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
        Appointment, #type:ignore
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

    session = models.CharField(max_length=255)
    items = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #def __str__(self):
    #    return f"Payment {self.id} - {self.patient.username} - {self.status}"

    #@property
    #def customer_name(self):

    #@property
    #def customer_email(self):
