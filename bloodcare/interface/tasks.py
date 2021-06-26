
from config import celery_app

import time

@celery_app.task()
def auto_call_trigger(data,receipient):
    """Triggering twilio api to call certain person"""
    for donor in data.items():
        print(donor,receipient)
        time.sleep(5)

    return None
