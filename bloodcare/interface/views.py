<<<<<<< HEAD

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
from django.utils.timezone import now

class PhoneNumberView(APIView):

    def get(self, request):
        return Response({"phone_no": "phone_no",
                         "latitude": 98.0,
                         "longitude": 98.0,
                         "zip_code": 695027,
                         "blood_group": "O+"
                         }, 200)

    def post(self, request):
        phone_no = request.data.get('phone_no', None)
        latitude = request.data.get('latitude', None)
        longitude = request.data.get('longitude', None)
        zipcode = request.data.get('zip_code', None)
        blood_group = request.data.get('blood_group', None)
        if not blood_group:
            return Response({"message": "Invalid Blood Group"}, 400)
        if not ((latitude and longitude) or zipcode):
            return Response({"Location Info is Not Given"}, 400)

        if phone_no:
            otp = Recipient.generate_otp()
            # TODO Send OTP Via Celery
            otp_object = Recipient.objects.get(phone_no=phone_no)
            if otp_object:
                otp_object.otp = otp
                otp_object.count += 1
            otp_object = Recipient(otp=otp, phone_no=phone_no)
            otp_object.last_used = now()
            otp_object.save()
            return Response({"message": "OTP Sent"}, 200)
        return Response({"message": "Invalid Key"}, 400)


phone_number_view = PhoneNumberView.as_view()


class OTPVerificationView(APIView):

    def get(self, request):
        return Response({"otp": "otp",
                         "phone_no": "phone"}, 200)

    def post(self, request):
        data = request.data
        otp = data.get('otp', None)
        phone = data.get('phone_no', None)
        if otp:
            otp_object = Recipient.objects.get(phone_no=phone)
            if otp_object:
                if otp_object.otp == otp:
                    return Response({"message": "OTP Verified",
                                     "token": otp_object.key}, 200)
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

        
        