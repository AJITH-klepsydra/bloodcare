import binascii
import os

from django.db import models

from bloodcare.donor.models import Donor
from bloodcare.interface.models import Recipient


# Create your models here.


class Link(models.Model):
    recipient = models.ForeignKey(Recipient, on_delete=models.PROTECT)
    donor = models.ForeignKey(Donor, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return f'{self.recipient.phone_no} -> {self.donor.name}'

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_key()
        return super(Link, self).save(*args, **kwargs)


class Status(models.Model):
    status = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    detail = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.status}. {self.detail}"
