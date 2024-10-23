from django.http import JsonResponse
from django.shortcuts import render
from .models import Catalogo
import json

# Create your views here.


def home(request):
    catalogo = Catalogo.objects.all().order_by('-pk')
    return render(request, 'home.html',{
        'productos': catalogo,
    })


def catalogo(request):
    catalogo = Catalogo.objects.all().order_by('-pk')
    return render(request, "catalogo/catalogo.html", {
        'productos': catalogo,
    })


def stock(request):
    if request.method == 'GET':
        return render(request, "catalogo/crearcatalogo.html")
    if request.method == 'POST':
        data = json.loads(request.body)
        
        nombre_producto = data.get('nombre_producto')
        imagen_producto = data.get('imagen_producto')
        precio = data.get('precio')
        moneda_producto = data.get('moneda_producto')
        tamanno = data.get('tamanno')

        # Crea una nueva instancia del producto y guárdala
        product = Catalogo(
            nombre=nombre_producto,
            imagen=imagen_producto,
            precio=precio,
            moneda=moneda_producto,
            tamanno=tamanno,
        )
        
        product.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)



def modstock(request, product_id):
    catalogo = Catalogo.objects.get(pk=product_id)


    return render(request, "catalogo/modcatalogo.html", {
        'producto': catalogo,
    })