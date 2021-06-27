from rest_framework.serializers import ModelSerializer

from .models import Donor


class DonorSerializer(ModelSerializer):
    class Meta:
        model = Donor
        fields = ('name', 'mobile_no')


class CustomDonorSerializer(ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'
