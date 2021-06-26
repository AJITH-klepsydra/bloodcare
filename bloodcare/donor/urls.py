from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter

from .views import (DonorViewSet, )

api_router = DefaultRouter()
api_router.register('', DonorViewSet, 'donor')

urlpatterns = [
    path("", include((api_router.urls, "donors")), name="donor_view"),
]

from django.conf import settings
if settings.DEBUG:
    from .seed import donor_add
    urlpatterns +=[path("add/donors/",view=donor_add,name="add new donors"),]