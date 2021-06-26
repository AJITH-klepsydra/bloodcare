from django.db.models import manager
from bloodcare.interface.models import Recipient
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from .models import Donor
from .decorators import is_authenticated
from rest_framework.viewsets import GenericViewSet
# Create your views here.
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView
from .serializers import DonorSerializer


class DonorViewSet(ListModelMixin, GenericViewSet):
    serializer_class = DonorSerializer

    def get_queryset(self):
        token = self.request.headers.get("key",None)
        if not token:
            return Response({"message":"unAuthorized."},status=401)
        return Donor.objects.all()

class DonorView(APIView):
    @is_authenticated
    def get(self,request):
        v = self.request.user
        data = Donor.objects.get_n_closest_loc(v,5)    
        ser = DonorSerializer(data=data,many=True)
        ser.is_valid()
        return Response(ser.data,status=200)

donor_view = DonorView.as_view()