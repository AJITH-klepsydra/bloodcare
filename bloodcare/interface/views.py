from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework import status
from .serializers import RecipientSerializer


class PhoneNumberView(APIView):

    def get(self, request):
        return Response({"phone_no": "phone_no",
                         "latitude": 98.0,
                         "longitude": 98.0,
                         "zip_code": 695027
                         }, 200)

    def post(self, request):
        res = RecipientSerializer(data = request.data)
        if res.is_valid():
            phone_no = res.validated_data.get('phone_no', None)
            latitude = res.validated_data.get('latitude', None)
            longitude = res.validated_data.get('longitude', None)
            zipcode = res.validated_data.get('zip_code', None)
            if not ((latitude and longitude) or zipcode):
                return Response({"Location Info is Not Given"},400)
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
