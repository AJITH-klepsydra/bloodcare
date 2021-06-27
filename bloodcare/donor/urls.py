from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from .seed import donor_add
from .views import (DonorViewSet, donor_view)

api_router = DefaultRouter()
api_router.register('', DonorViewSet, 'donor')

urlpatterns = [
    path("", view=donor_view, name="donor_view"),
    path("all/", include((api_router.urls, "donors")), name="donor_view_set"),
    path("add/", view=donor_add, name="add new donors"),
]
