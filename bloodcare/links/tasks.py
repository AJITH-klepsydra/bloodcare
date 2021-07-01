from django.conf import settings
from twilio.rest import Client

from config import celery_app


@celery_app.task()
def send_message(ph_no, message):
    """Sending Message"""
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=message,
        from_=settings.FROM,
        to=ph_no
    )
