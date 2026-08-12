from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),  # ← AGREGAR ESTA LÍNEA (URL raíz)
    path("homepage/", include("homepage.urls")),
    path("landing/api/", include("landing_api.urls")),
    path("demo/rest/api/", include("demo_rest_api.urls")),
]