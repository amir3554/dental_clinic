# Schedule automatic sending
from celery import shared_task
from django.utils import timezone
from .models import Notification


@shared_task
def send_due_notifications():
    now = timezone.now()
    due = Notification.objects.filter(status='pending', send_at__lte=now)
    for notif in due:
        try:
            notif.send()
        except:
            pass
