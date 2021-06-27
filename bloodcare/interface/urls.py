from django.urls import path

from .views import phone_number_view, otp_view,twilio_call,twilio_status

app_name = "interface"

urlpatterns = [
    path('', phone_number_view, name='registration', ),
    path('valid/', otp_view, name='otp', ),
    path('autocall/', twilio_call, name='twilio_call', ),
    path('autocall/status/<str:twilio_token>/', twilio_status, name='twilio_status', ),
]
