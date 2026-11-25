from django.urls import path
from . import views

app_name = "bicicletas"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("bicicletas/", views.listar, name="listar"),
    path("bicicletas/nueva/", views.crear, name="crear"),
    path("bicicletas/<int:pk>/editar/", views.editar, name="editar"),
    path("bicicletas/<int:pk>/eliminar/", views.eliminar, name="eliminar"),
]
