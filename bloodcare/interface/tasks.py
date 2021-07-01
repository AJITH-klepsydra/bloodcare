import time

from django.conf import settings
from twilio.rest import Client

from bloodcare.links.models import Link
from config import celery_app
from .models import Recipient


@celery_app.task()
def auto_call_trigger(data, recipient):
    """Triggering twilio api to call certain person"""
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    for donor in data:
        call_message = f""
        call = client.calls.create(twiml=f'<Response><Say>{call_message}</Say></Response>',
                                   to=donor.mobile_no,
                                   from_=settings.FROM)

        link = Link(recipient=recipient["recipient"], donor=donor, status="CALL TRIGGERED")
        link.save()

        text_message = f"bloodcare.csitkmce.tech\\links\\{link.slug}"

        message = client.messages.create(
            body=text_message,
            from_=settings.FROM,
            to=donor.mobile_no
        )
        print(donor, recipient)
        time.sleep(10)
        # TODO: Twilio call integration
    try:
        Recipient.objects.get(twilio_id=recipient['twilio_token']).change_twilio_status()
    except:
        pass
    return None
