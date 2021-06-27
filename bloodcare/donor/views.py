from rest_framework import permissions
# Create your views here.
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .decorators import is_authenticated
from .models import Donor
from .serializers import DonorSerializer


class DonorViewSet(ListModelMixin, GenericViewSet):
    serializer_class = DonorSerializer
    permission_classes = [permissions.IsAdminUser, ]

    def get_queryset(self):
        return Donor.objects.all()


class DonorView(APIView):
    """
           Retrieves n closest Donors

           Authenticated View Pass Auth Token as header Authorization

           GET

           RESPONSE

           LIST OF DONORS

           [ <br>
           &nbsp;&nbsp;&nbsp;&nbsp;     {<br>
           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         "name": "Ajith",<br>
           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         "mobile_no": "+918943234482"<br>
           &nbsp;&nbsp;&nbsp;&nbsp;     },<br>
           &nbsp;&nbsp;&nbsp;&nbsp;     {<br>
           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         "name": "Arun kumar P M",<br>
           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         "mobile_no": "+918943235482"<br>
           &nbsp;&nbsp;&nbsp;&nbsp;     }<br>
            ]<br>

           STATUS CODE

           200 - List of users <br>
           400 - Not Authenticated


           """

    @is_authenticated
    def get(self, request):
        v = self.request.user
        data = Donor.objects.get_n_closest_loc(v, 5)
        ser = DonorSerializer(data=data, many=True)
        ser.is_valid()
        return Response(ser.data, status=200)


donor_view = DonorView.as_view()
