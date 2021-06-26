from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path,include
from bloodcare.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls

urlpatterns += [path("register/", include("bloodcare.interface.urls"), name="interface"),
                path("donors/", include("bloodcare.donor.urls"), name="donors"),
                ]
