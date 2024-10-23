from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('catalogo/', views.catalogo, name="catalogo"),
    path('annadir-catalogo/', views.stock, name="createcatalogo"),
]