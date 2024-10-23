from django.urls import path, include
from . import views


urlpatterns = [
    path('productos/', views.producto, name="productos"),
    path('factura/', views.factura, name="facturas"),
    path('productos/<int:product_id>/', views.modificar, name="modificar"),
    path('clientes/', views.cliente, name="clientes"),
    path('clientes/<str:numero_wsp>', views.modcliente, name="modcliente"),
    path('clientes/<str:numero_wsp>/<str:fecha>/', views.modificar_factura, name='modificar_factura')
]