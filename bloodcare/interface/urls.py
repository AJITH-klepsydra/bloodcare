from django.urls import path

from .views import phone_number_view, otp_view,twilio_call

app_name = "interface"

urlpatterns = [
    path('', phone_number_view, name='registration', ),
    path('valid/', otp_view, name='otp', ),
    path('autocall/<str:phone_no>/', twilio_call, name='twilio_call', ),
]
