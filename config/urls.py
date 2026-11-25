from django.urls import include, path

urlpatterns = [
    path("", include("bicicletas.urls")),
]
