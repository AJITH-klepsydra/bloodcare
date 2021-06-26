from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framwork import status


class PhoneNumberView(APIView):

    def get(self, request):
        return Response({"phone_no": "phone_no",
                         "latitude": 98.0,
                         "longitude": 98.0,
                         "zipcode": 695027
                         }, 200)

    def post(self, request):
        data = request.data
        phone_no = data.get('phone_no', None)
        latitude = data.get('latitude', None)
        longitude = data.get('longitude', None)
        zipcode = data.get('zipcode', None)
        if not ((latitude and longitude) or zipcode):
            return Response({"Location Info is Not Given"},400)
        if phone_no:
            # send_otp
            return Response({"message": "OTP Sent"}, 200)
        return Response({"message": "Invalid Field"}, 400)


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
