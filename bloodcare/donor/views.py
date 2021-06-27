from django.shortcuts import render
from .models import Donor

from rest_framework.viewsets import GenericViewSet
# Create your views here.
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView
from .serializers import DonorSerializer
from rest_framework import permissions


class DonorViewSet(ListModelMixin, GenericViewSet):
    serializer_class = DonorSerializer

    def get_queryset(self):
        return Donor.objects.all()
