from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.timezone import now
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from bloodcare.donor.serializers import Donor, DonorSerializer
from .models import Recipient
from .tasks import auto_call_trigger
<<<<<<< HEAD
from django.utils.timezone import now
from bloodcare.donor.decorators import is_authenticated
=======


>>>>>>> 396e12976100125cf8aa4ac1d3b5a693c2e64944
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
            try:
                otp_object = Recipient.objects.get(phone_no=phone_no)
            except:
                otp_object = None
            if otp_object:
                otp_object.otp = otp
                otp_object.count += 1
            otp_object = Recipient(otp=otp, phone_no=phone_no)
            otp_object.last_used = now()
            otp_object.latitude = latitude
            otp_object.longitude = longitude
            otp_object.zip_code = zipcode
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
            try:
                otp_object = Recipient.objects.get(phone_no=phone)
            except:
                otp_object = None
            if otp_object:
                if otp_object.otp == otp:
                    return Response({"message": "OTP Verified",
                                     "token": otp_object.key}, 200)
            return Response({"message": "OTP Invalid"}, 400)
        return Response({"message": "Invalid Field"}, 400)


otp_view = OTPVerificationView.as_view()


class TwilioCall(APIView):
    @is_authenticated
    def get(self,request):
        return Response({"phone_no":"+918943234482"},status=200)
    @is_authenticated    
    def post(self,request):
        phone_no = request.data.get('phone_no')
        recipient = get_object_or_404(Recipient,phone_no=phone_no)
        if recipient.twilio_id:
            return Response({"status":"There is an ongoing call service"},status=status.HTTP_226_IM_USED)
        recipient.twilio_id = f"BC_AUTO_{recipient.generate_key()}"
        recipient.save()
        donors = Donor.objects.get_n_closest_loc(recipient,15)
        data = DonorSerializer(donors,many=True).data
        auto_call_trigger.delay(data,{"reciepient_no":str(recipient.phone_no),"twilio_token":recipient.twilio_id})
        
        return Response({"twilio_token":recipient.twilio_id},status=status.HTTP_201_CREATED)
    
twilio_call = TwilioCall.as_view()

class TwilioStatus(APIView):
    @is_authenticated 
    def get(self,request,twilio_token):
        try:
            receipient = Recipient.objects.get(twilio_id=twilio_token)
        except:
            return Response({"status":"No valid ongoing AutoCall service!!"},status=status.HTTP_200_OK)
        
        return Response({"twilio_token":"Ther is an Ongoing Call"},status=status.HTTP_204_NO_CONTENT)
    
twilio_status = TwilioStatus.as_view()

        
