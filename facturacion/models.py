from django.db import models

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length=200, default="Cliente")
    numero_wsp = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.numero_wsp


class Producto(models.Model):
    fecha = models.DateField(auto_now_add=True)
    nombre_producto = models.CharField(max_length=200)
    enlace_temu = models.CharField(max_length=300)
    cantidad = models.IntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tipo_pago = models.CharField(max_length=200)
    peso = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    encargado = models.BooleanField(default=False)
    recibido = models.BooleanField(default=False)
    entregado = models.BooleanField(default=False)
    factura = models.ForeignKey(Cliente, on_delete=models.CASCADE, to_field='numero_wsp')
    cambio_cup = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cambio_mlc = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nota = models.TextField(default="")


    @property
    def total(self):
        return self.precio * self.cantidad
    def total_cup(self):
        return self.total * self.cambio_cup
    def total_mlc(self):
        return self.total * self.cambio_mlc
    
    

    def fecha_formateada(self):
        return self.fecha.strftime('%d/%m/%Y')
    

