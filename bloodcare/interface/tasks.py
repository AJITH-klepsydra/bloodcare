import time

from django.conf import settings
from twilio.rest import Client
from bloodcare.links.models import Link
from config import celery_app
from .models import Recipient



from bloodcare.interface.models import Recipient
from bloodcare.donor.models import Donor
@celery_app.task()
def auto_call_trigger(data, recipient):
    """Triggering twilio api to call certain person"""
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    for donor in data:
    
            call_message = f"this is an important message f"
            call = client.calls.create(twiml=f'<Response><Play loop="2">https://russet-otter-8490.twil.io/assets/bloodcare.mp3</Play></Response>',
                                    to=donor['mobile_no'],
                                    from_=settings.FROM)
            rec_obj = Recipient.objects.get(pk=recipient["recipient"])
            don_obj = Donor.objects.get(pk=donor['id'] )
            link = Link(recipient=rec_obj, donor=don_obj,)
            link.save()

            text_message = f"127.0.0.1:3000/links/{link.slug}"

            message = client.messages.create(
                body=text_message,
                from_=settings.FROM,
                to=donor['mobile_no']
            )

       
    try:
        Recipient.objects.get(twilio_id=recipient['twilio_token']).change_twilio_status()
    except:
        pass
    return None
