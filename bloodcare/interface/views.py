from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Recipient


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
