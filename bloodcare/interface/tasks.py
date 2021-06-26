
from rest_framework.fields import RegexField
from config import celery_app
from .models import Recipient
import time

@celery_app.task()
def auto_call_trigger(data,receipient):
    """Triggering twilio api to call certain person"""
    for donor in data:
        print(donor,receipient)
        time.sleep(10)
        # TODO: Twilio call integration
    try:
        Recipient.objects.get(twilio_id = receipient['twilio_token']).change_twilio_status()
    except:
        pass
    return None
