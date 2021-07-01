from django.db import models
from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from .models import Status
class StatSerializer(ModelSerializer):

    class Meta:
        model = Status
        fields = "__all__"
        depth = 1

