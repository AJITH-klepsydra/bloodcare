from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from bloodcare.interface.models import Recipient
from .haversine import closest


class DonorManager(models.Manager):
    def get_n_closest_loc(self, v):
        if not v and not v.blood_group:
            return None
        data = Donor.objects.all().filter(blood_group=v.blood_group)
        return closest(data, v, 10)


class Donor(models.Model):
    name = models.CharField(max_length=250, default="Donor")
    mobile_no = PhoneNumberField(_("Mobile number: "))
    email = models.EmailField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    pin_code = models.IntegerField(null=True, blank=True)
    distict = models.CharField(max_length=200, null=True, blank=True)
    subdistrict = models.CharField(max_length=200, null=True, blank=True)
    last_donated = models.DateTimeField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    blood_group = models.CharField(max_length=100)
    date_of_joined = models.DateTimeField(auto_now_add=True)
    objects = DonorManager()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self) -> str:
        return f"< {self.name} > #ph-{self.mobile_no}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
