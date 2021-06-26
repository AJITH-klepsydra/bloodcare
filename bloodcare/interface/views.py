from rest_framework.response import Response

from rest_framework.views import APIView


class PhoneNumberView(APIView):

    def get(self, request):
        return Response({"phone_no": "phone_no"}, 200)

    def post(self, request):
        data = request.data
        phone_no = data.get('phone_no', None)
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
