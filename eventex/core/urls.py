from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.home, name="home"),
    path('palestrantes/<slug:slug>/', views.speaker_detail, name="speaker-detail"),
]
