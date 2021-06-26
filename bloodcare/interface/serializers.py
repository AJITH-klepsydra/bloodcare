from rest_framework.serializers import ModelSerializer

from .models import Recipient


class RecipientSerializer(ModelSerializer):
    class Meta:
        model = Recipient
        fields = ('phone_no', 'latitude', 'longitude', 'zip_code')
