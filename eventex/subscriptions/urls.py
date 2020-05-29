from django.urls import path
from . import views


app_name = "subscriptions"

urlpatterns = [
    path("", views.subscribe, name="subscribe"),
    path("obrigado/<uuid:uuid>/", views.thanks, name="thanks"),
]
