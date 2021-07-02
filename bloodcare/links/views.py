from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Link
from .models import Status
from .tasks import send_message


class LinkManageView(APIView):
    def get(self, request, link):
        obj = get_object_or_404(Link, slug=link)
        obj.status = "Donor Visited the Website"
        if not Status.objects.filter(detail = str(obj.donor.name)):
            status = Status(status=obj.recipient, detail=f"{obj.donor.name}")
            status.save()
            obj.save()

            message = f"Call Me Bro {obj.donor.mobile_no}, I will give you damn blood"
            send_message.delay(str(obj.recipient.phone_no), message)
            return Response({"message": f"Successfully Marked. Contact : {obj.recipient.phone_no} for donating {obj.recipient.blood_group} Blood"}, 200)
        
        return Response({"message":"Already reported"},status=200)

link_manage_view = LinkManageView.as_view()
