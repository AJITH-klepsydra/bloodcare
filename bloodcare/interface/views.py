from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.views import APIView

from bloodcare.donor.decorators import is_authenticated
from bloodcare.donor.serializers import Donor, DonorSerializer
from .models import Recipient
from .tasks import auto_call_trigger


class PhoneNumberView(APIView):
    """
    Accepts Recipient Details and Sends an OTP to the user

    POST

    { <br>
    &nbsp;&nbsp;&nbsp;&nbsp;    "phone_no": "+911234567890",<br>
    &nbsp;&nbsp;&nbsp;&nbsp;    "latitude": 98.0,<br>
    &nbsp;&nbsp;&nbsp;&nbsp;    "longitude": 98.0,<br>
    &nbsp;&nbsp;&nbsp;&nbsp;    "zip_code": 695027,<br>
    &nbsp;&nbsp;&nbsp;&nbsp;    "blood_group": "O+"<br>
    }<br>

    RESPONSE

    {<br>
    &nbsp;&nbsp;&nbsp;&nbsp;    "message" : "message"<br>
    }<br>

    STATUS CODE

    200 - OTP Send<br>
    400 - Auth Issues


    """

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
    """
       Validate OTP and Authenticate the user

       POST

       { <br>
       &nbsp;&nbsp;&nbsp;&nbsp;    "otp": "12345678",<br>
       &nbsp;&nbsp;&nbsp;&nbsp;    "phone_no": "911234567890",<br>
       }<br>

       RESPONSE

       {<br>
       &nbsp;&nbsp;&nbsp;&nbsp;    "message" : "message"<br>
       &nbsp;&nbsp;&nbsp;&nbsp;    "token" : "token"<br>
       }<br>

       STATUS CODE

       200 - Send Token if OTP is Valid
       400 - OTP Invalid


       """

    def get(self, request):
        return Response({"otp": "otp",
                         "phone_no": "phone"}, 200)

    def post(self, request):
        data = request.data
        otp = data.get('otp', None)
        phone = data.get('phone_no', None)
        if otp and phone:
            if not type(otp) == int:
                return Response({"message": "OTP Field must be a integer"}, 400)
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
    def get(self, request):
        return Response({"phone_no": "+918943234482"}, status=200)

    @is_authenticated
    def post(self, request):
        phone_no = request.data.get('phone_no')
        recipient = get_object_or_404(Recipient, phone_no=phone_no)
        if recipient.twilio_id:
            return Response({"status": "There is an ongoing call service"}, status=status.HTTP_226_IM_USED)
        recipient.twilio_id = f"BC_AUTO_{recipient.generate_key()}"
        recipient.save()
        donors = Donor.objects.get_n_closest_loc(recipient, 15)
        data = DonorSerializer(donors, many=True).data
        auto_call_trigger.delay(data, {"reciepient_no": str(recipient.phone_no), "twilio_token": recipient.twilio_id})

        return Response({"twilio_token": recipient.twilio_id}, status=status.HTTP_201_CREATED)


twilio_call = TwilioCall.as_view()


class TwilioStatus(APIView):
    @is_authenticated
    def get(self, request, twilio_token):
        try:
            receipient = Recipient.objects.get(twilio_id=twilio_token)
        except:
            return Response({"status": "No valid ongoing AutoCall service!!"}, status=status.HTTP_200_OK)

        return Response({"twilio_token": "Ther is an Ongoing Call"}, status=status.HTTP_204_NO_CONTENT)


twilio_status = TwilioStatus.as_view()
