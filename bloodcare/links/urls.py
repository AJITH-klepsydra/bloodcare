from django.urls import path

from .views import link_manage_view

app_name = "links"
urlpatterns = [
    path("<slug:link>/", view=link_manage_view, name="link_view"),
]
