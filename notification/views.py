from django.shortcuts import render
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from .models import NotificationTemplate, Notification
from clinic.models import Appointment



# Create pre-appointment notifications

@receiver(post_save, sender=Appointment)
def schedule_reminders(sender, instance, created, **kwargs):
    if created:
        # قبل يوم
        Notification.objects.create(
            template=NotificationTemplate.objects.get(name='reminder_1day'),
            context={'appointment': instance},
            send_at=instance.date - timedelta(days=1),
        ).recipients.add(instance.patient)

        # قبل ساعة
        Notification.objects.create(
            template=NotificationTemplate.objects.get(name='reminder_1hour'),
            context={'appointment': instance},
            send_at=instance.date - timedelta(hours=1),
        ).recipients.add(instance.patient)


