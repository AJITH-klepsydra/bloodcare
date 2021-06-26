
from rest_framework.response import Response
from .models import Recipient
from rest_framework.views import APIView
from rest_framework import status
from .serializers import RecipientSerializer
from rest_framework import permissions
from django.shortcuts  import get_object_or_404
from bloodcare.donor.models import Donor
from bloodcare.donor.serializers import Donor, DonorSerializer
from django.utils import timezone
from .tasks import auto_call_trigger
class PhoneNumberView(APIView):

    def get(self, request):
        return Response({"phone_no": "phone_no",
                         "latitude": 98.0,
                         "longitude": 98.0,
                         "zip_code": 695027,
                         "blood_group": "O+"

                         }, 200)

    def post(self, request):
        res = RecipientSerializer(data=request.data)
        if res.is_valid():
            phone_no = res.validated_data.get('phone_no', None)
            latitude = res.validated_data.get('latitude', None)
            longitude = res.validated_data.get('longitude', None)
            zipcode = res.validated_data.get('zip_code', None)
            blood_group = res.validated_data.get('blood_group', None)
            if not ((latitude and longitude) or zipcode):
                return Response({"Location Info is Not Given"}, 400)
            if phone_no:
                # send_otp
                res.save()
                return Response({"message": "OTP Sent"}, 200)
        return Response(res.errors, 400)


phone_number_view = PhoneNumberView.as_view()


class OTPVerificationView(APIView):

    def get(self, request):
        return Response({"otp": "otp"}, 200)

    def post(self, request):
        data = request.data
        otp = data.get('otp', None)
        if otp:
            valid = True
            if valid:
                return Response({"message": "OTP Verified"}, 200)
            return Response({"message": "OTP Invalid"}, 400)
        return Response({"message": "Invalid Field"}, 400)


otp_view = OTPVerificationView.as_view()


class TwilioCall(APIView):
    permission_classes = [permissions.AllowAny,]
    def get(self,request,phone_no):
        recipient = get_object_or_404(Recipient,phone_no=phone_no)
        recipient.twilio_id = f"BC_AUTOCALL_{recipient.id}_{timezone.now}"
        recipient.save()
        donors = Donor.objects.get_n_closest_loc(recipient,15)[5:]
        data = DonorSerializer(donors,many=True).data
        auto_call_trigger.delay(data,{"reciepient_no":recipient.phone_no,"twilio_token":recipient.twilio_id})
        
        return Response({"twilio_token":recipient.twilio_id},status=200)
    def post(self,request,twilio_token):
        pass
        
twilio_call = TwilioCall.as_view()

        
        