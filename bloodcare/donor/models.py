from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class DonorManager(models.Manager):
    pass


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
    blood_group = models.CharField(max_length=5)
    date_of_joined = models.DateTimeField(auto_now_add=True)
    objects = DonorManager()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self) -> str:
        return f"< {self.name} > #ph-{self.mobile_no}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
