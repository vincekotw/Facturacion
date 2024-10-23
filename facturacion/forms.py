from django import forms
from .models import Cliente, Producto

class CrearNuevaFactura(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'enlace_temu', 'cantidad', 'precio', 'tipo_pago', 'peso']


class BuscarCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['numero_wsp',]

class ActualizarEstado(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['encargado', 'recibido', 'entregado',]

class ModificarProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['factura', 'nombre_producto', 'enlace_temu', 'cantidad', 'precio', 'tipo_pago', 'peso', 'encargado', 'recibido', 'entregado',]

class ModificarCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'numero_wsp',]