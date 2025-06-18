from django.db import models
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from datetime import timedelta


class NotificationStatus(models.IntegerChoices):
    PENDING = 1, 'pending'
    SENT = 2, 'sent'
    FAILED = 3, 'failed'




class NotificationTemplate(models.Model):
    """
    قالب رسالة الإشعار.
    يمكنك ربطه بأي نوع رسالة (تأكيد حجز، تذكير، إلخ).
    """
    name = models.CharField(max_length=100, unique=True)
    subject_template = models.CharField(
        max_length=200,
        help_text="صيغة عنوان الإيميل مع متغيرات مثل {{ appointment.date }}"
    )
    html_template_path = models.CharField(
        max_length=200,
        help_text="مسار ملف القالب داخل templates، مثلاً 'emails/appointment_confirmation.html'"
    )
    text_template_path = models.CharField(
        max_length=200,
        blank=True, null=True,
        help_text="مسار قالب نصي بسيط (اختياري)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Notification(models.Model):
    """
    رسالة إشعار واحدة توجه لمستخدم أو أكثر،
    مبنية على NotificationTemplate، مع سياق (context) لتمرير البيانات للقالب.
    """
    # ربط عام بكائن مثل Appointment أو أي نموذج آخر
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True, null=True
    )

    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    template = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.PROTECT,
        related_name='notifications'
    )
    recipients = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='notifications'
    )
    context = models.JSONField(
        help_text="بيانات لتمريرها للقالب، مثلاً {'appointment': appointment, 'user': user}"
    )


    status = models.IntegerField(
        choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING
    )
    
    error_msg   = models.TextField(blank=True, null=True)
    sent_at     = models.DateTimeField(blank=True, null=True)

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.template.name} → {self.recipients.count()} user(s) [{self.status}]"

    def send(self):
        """
        ينشئ ويرسل الإيميل ثم يحدث الحالة.
        """
        try:
            # توليد العنوان
            subject = render_to_string(
                self.template.subject_template, self.context
            ).strip()

            # توليد النص العادي إذا وُجد
            text_body = None
            if self.template.text_template_path:
                text_body = render_to_string(
                    self.template.text_template_path, self.context
                )

            # توليد HTML
            html_body = render_to_string(
                self.template.html_template_path, self.context
            )

            # إنشاء رسالة متعددة الأجزاء
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_body or "",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[u.email for u in self.recipients.all()],
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send()

            # تحديث الحالة
            self.status  = 'sent'
            self.sent_at = timezone.now()
            self.save(update_fields=['status', 'sent_at'])
        except Exception as e:
            self.status    = 'failed'
            self.error_msg = str(e)
            self.save(update_fields=['status', 'error_msg'])
            raise

    class Meta: 
        ordering = ['-created_at']



"""
1.NotificationTemplate

* It retains the template name, title sentences, and HTML templates (and optional plain text).

* You can create any number of templates
(booking confirmation, reminder, cancellation notice, etc.).

2.Notification

* It is linked to the template via FK.

* It stores recipients (ManyToMany to users).

* It stores a context as JSON to pass reservation or user data.

* You can bind it to any object (for example, Appointment) via GenericForeignKey.

* It contains a status field to track whether the message was sent or failed.

* The send() function constructs the email header, body,
and HTML and sends it via EmailMultiAlternatives, then updates the status.


"""
