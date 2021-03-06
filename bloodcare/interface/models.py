import binascii
import os
from random import randint

from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Recipient(models.Model):
    phone_no = PhoneNumberField(_("Mobile number: "))
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    blood_group = models.CharField(max_length=100, default="O+")
    twilio_id = models.CharField(max_length=50, editable=False, blank=True, null=True)
    blood_group = models.CharField(max_length=5, default="O+")
    otp = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField()
    key = models.CharField(_("Key"), max_length=40, primary_key=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Recipient, self).save(*args, **kwargs)

    def change_twilio_status(self):
        self.twilio_id = None
        self.save()

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    @staticmethod
    def generate_otp():
        return randint(10000000, 99999999)

    def __str__(self):
        return str(self.phone_no)
