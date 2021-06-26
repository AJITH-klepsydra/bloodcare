from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class Recipient(models.Model):
    phone_no = PhoneNumberField(_("Mobile number: "))
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.phone_no)
