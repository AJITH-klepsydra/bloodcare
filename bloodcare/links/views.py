from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Link
from .models import Status
from .tasks import send_message


class LinkManageView(APIView):
    def get(self, request, link):
        obj = get_object_or_404(Link, link)
        obj.status = "Donor Visited the Website"

        status = Status(status=obj.recipient, detail=f"{obj.donor.name} Accepted")
        status.save()
        obj.save()

        message = f"Call Me Bro {obj.donor.mobile_no}, I will give you damn blood"
        send_message.delay(obj.recipient.phone_no, message)
        return Response({"message": "Successfully Marked"}, 200)


link_manage_view = LinkManageView.as_view()
