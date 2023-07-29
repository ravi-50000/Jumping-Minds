from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

@shared_task(bind=True)
def send_email(self, subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)
