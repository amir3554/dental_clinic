# celery.py
# beat schedule:

from celery.schedules import crontab
from dental_clinic_project import settings

settings.beat_schedule = {
    'send-notifications-every-minute': {
        'task': 'notification.tasks.send_due_notifications',
        'schedule': crontab(),  # كل دقيقة
    },
}
