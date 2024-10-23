from django.db import models

# Create your models here.
class Catalogo(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imagen = models.CharField(max_length=500)
    tamanno = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    moneda = models.CharField(max_length=10)
    fecha = models.DateTimeField(auto_now_add=True)
