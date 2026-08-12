from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.LandingAPI.as_view(), name="landing-index"),
    path("index/<str:item_id>/", views.LandingDetailAPI.as_view(), name="landing-detail"),
]
