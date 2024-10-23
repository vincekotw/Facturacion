from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Cliente, Producto
from .forms import CrearNuevaFactura, BuscarCliente, ActualizarEstado, ModificarProducto, ModificarCliente
import json
from django.http import JsonResponse
import datetime



# Create your views here.
def producto(request):
    # Inicializar la consulta de productos
    productos = Producto.objects.all()
    fechas = set()
    fecha_seleccionada = datetime.date.today()


    if request.method == 'GET':
        productos = productos.filter(encargado=False)
        estado_actual = "por encargar"
        
    if request.method == 'POST':
        form_name = request.POST['form_name']
        
        if form_name == 'form2':
            form = ActualizarEstado(request.POST)
            if form.is_valid():
                estado_actual = request.POST.get('estado_actual', '')
                producto = Producto.objects.get(pk=request.POST['id'])
                encargado = form.cleaned_data['encargado']
                recibido = form.cleaned_data['recibido']
                entregado = form.cleaned_data['entregado']
                if entregado:
                    producto.encargado = entregado
                    producto.recibido = entregado
                    producto.entregado = entregado                
                elif recibido:
                    producto.encargado = recibido
                    producto.recibido = recibido
                    producto.entregado = entregado
                elif encargado:
                    producto.encargado = encargado
                    producto.recibido = recibido
                    producto.entregado = entregado
                producto.save()

        elif form_name == 'form1':
            query = request.POST.get('buscar')
            clientes = Cliente.objects.all()
            if query:
                clientes = clientes.filter(
                    Q(numero_wsp__icontains=query)
                ).values_list('numero_wsp', flat=True)
                productos = productos.filter(
                    Q(factura__numero_wsp__icontains=clientes) |
                    Q(nombre_producto__icontains=query) |
                    Q(enlace_temu__icontains=query)
                )

        elif form_name == "form3":
            estado_actual = request.POST['estado']
            if estado_actual == "por encargar":
                productos = productos.filter(encargado=False)
            elif estado_actual == "encargado":
                productos = productos.filter(encargado=True, recibido=False, entregado=False)
            elif estado_actual == "recibido":
                productos = productos.filter(recibido=True, entregado=False)
            elif estado_actual == "entregado":
                productos = productos.filter(entregado=True)
            else:
                productos = Producto.objects.all()
        
        elif form_name == "form4":
            estado_actual = request.POST.get('estado_actual', '')
            fecha_seleccionada = request.POST.get('fecha', None)
            if fecha_seleccionada:
                productos = productos.filter(fecha=fecha_seleccionada)

    # Agrupar productos por fecha
    for product in productos:
        if product.fecha is not None:  # Verificar si la fecha es válida
            fechas.add(product.fecha)

    # Crear un diccionario para agrupar productos por fecha
    productos_por_fecha = {}
    for fecha in fechas:
        productos_por_fecha[fecha] = productos.filter(fecha=fecha)

    # Calcular la diferencia en días y el porcentaje de progreso
    progreso = {}
    dias = {}
    today = datetime.date.today()
    for fecha in fechas:
        if fecha is not None:  # Verificar si la fecha es válida
            dias_transcurridos = (today - fecha).days
            porcentaje = (dias_transcurridos / 28) * 100 if dias_transcurridos <= 28 else 100
            progreso[fecha] = min(porcentaje, 100)
            dias[fecha] = dias_transcurridos
        else:
            progreso[fecha] = 0
            dias[fecha] = 0

    return render(request, 'facturas/productos.html', {
        'producto': productos,
        'estado': ActualizarEstado,
        'fechas': sorted(fechas, reverse=True),
        'estado_actual': estado_actual,
        'productos_por_fecha': productos_por_fecha,  # Pasar el diccionario a la plantilla
        'fecha_seleccionada': fecha_seleccionada,
        'progreso': progreso,
        'dias': dias,
    })


def factura(request):
    if request.method == 'GET':
        return render(request, 'facturas/factura.html', {
            'factura':CrearNuevaFactura,
        })
    if request.method == 'POST':
        data = json.loads(request.body)
        numero_wsp = data.get('numero_wsp')
        productos_data = data.get('productos')

        cliente, created = Cliente.objects.get_or_create(numero_wsp=numero_wsp)

        for prod in productos_data:
            Producto.objects.create(
                nombre_producto=prod['nombre'],
                enlace_temu=prod['enlace_temu'],
                cantidad=prod['cantidad'],
                precio=prod['precio'],
                peso=prod['peso'],
                tipo_pago=prod['tipo_pago'],
                nota=prod['nota'],
                cambio_cup=prod["cambio_cup"],
                cambio_mlc=prod["cambio_mlc"],
                factura=cliente
            )
        return JsonResponse({'success': True})

    
def modificar(request, product_id):
    producto = Producto.objects.get(pk=product_id)
    factura = Cliente.objects.all()
    siguiente = producto.pk + 1
    anterior = producto.pk - 1
    while (siguiente <= Producto.objects.count() and not Producto.objects.filter(pk=siguiente).exists()):
        siguiente += 1
    while anterior >= 1 and not Producto.objects.filter(pk=anterior).exists():
        anterior -= 1
    modificar = ModificarProducto(instance=producto)
        
    if request.method == 'POST':
        if 'eliminar' in request.POST:
            producto.delete()
            return redirect('/productos/')
        if 'actualizar' in request.POST:
            form = ActualizarEstado(request.POST)
            if form.is_valid():
                encargado = form.cleaned_data['encargado']
                recibido = form.cleaned_data['recibido']
                entregado = form.cleaned_data['entregado']
                cliente_instace = Cliente.objects.get(numero_wsp=request.POST['factura'])
                producto.nombre_producto = request.POST['nombre_producto']
                producto.enlace_temu = request.POST['enlace_temu']
                producto.cantidad = request.POST['cantidad']
                producto.precio = request.POST['precio']
                producto.cambio_cup = request.POST['cambio_cup']
                producto.cambio_mlc = request.POST['cambio_mlc']
                if entregado:
                    producto.encargado = entregado
                    producto.recibido = entregado
                    producto.entregado = entregado                
                elif recibido:
                    producto.encargado = recibido
                    producto.recibido = recibido
                    producto.entregado = entregado
                elif encargado:
                    producto.encargado = encargado
                    producto.recibido = recibido
                    producto.entregado = entregado
                producto.tipo_pago = request.POST['tipo_pago']
                producto.factura = cliente_instace
                producto.save()
                return redirect('/productos/%s' %producto.pk)
    if Producto.objects.last().pk >= siguiente:
        return render(request, 'facturas/modificar.html', {
            'modificar':modificar,
            'producto':producto,
            'anterior':anterior,
            'siguiente':siguiente,
            'factura':factura
            })
    return render(request, 'facturas/modificar.html', {
            'modificar':modificar,
            'producto':producto,
            'anterior':anterior,
            'factura':factura
            })


def cliente(request):
    if request.method == 'GET':
        clientes = Cliente.objects.all()
        return render(request, 'facturas/clientes.html', {
            'clientes': clientes,            
        })
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            numero_wsp = data.get('numero_wsp')
            form_name = data.get('form_name') 
            if form_name == 'form1':
                cliente = Cliente.objects.get(numero_wsp=numero_wsp)
                productos = Producto.objects.filter(factura=cliente).order_by('fecha')
                productos_data = [
                    {
                        'nombre_producto': producto.nombre_producto,
                        'enlace_temu': producto.enlace_temu,
                        'cantidad': producto.cantidad,
                        'precio': float(producto.precio),
                        'total': float(producto.total),
                        'fecha': producto.fecha,
                        'encargado': producto.encargado,
                        'recibido': producto.recibido,
                        'entregado': producto.entregado,
                    }
                    for producto in productos
                ]
                return JsonResponse(productos_data, safe=False)
            else:
                return JsonResponse({'error': 'form_name no válido'}, status=400)

        except Cliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método de solicitud inválido'}, status=405)

        
def modcliente(request, numero_wsp):
    cliente = Cliente.objects.get(numero_wsp=numero_wsp)
    modificar = ModificarCliente(instance=cliente)
    if request.method == 'POST':
        if 'eliminar' in request.POST:
            cliente.delete()
            return redirect('/clientes/')
        if 'actualizar' in request.POST:
            cliente.nombre = request.POST['nombre']
            cliente.numero_wsp = request.POST['numero_wsp']
            cliente.save()
            return redirect('/clientes/%s' %cliente.numero_wsp)
    return render(request, 'facturas/modcliente.html', {
            'modificar':modificar,
            'cliente':cliente
        })
        

def modificar_factura(request, numero_wsp, fecha):
    cliente = Cliente.objects.get(numero_wsp=numero_wsp)
    productos = Producto.objects.filter(factura=cliente)
    productos.filter(fecha=fecha)
    if request.method == 'POST':
        for producto in productos:
            # Actualizar cada producto basado en los datos del formulario

            producto.nombre_producto = request.POST.get(f'nombre_producto_{producto.pk}')
            producto.enlace_temu = request.POST.get(f'enlace_temu_{producto.pk}')
            producto.cantidad = request.POST.get(f'cantidad_{producto.pk}')
            producto.precio = request.POST.get(f'precio_{producto.pk}')
            if f'cambio_cup_{producto.pk}' in request.POST:
                producto.cambio_cup = request.POST.get(f'cambio_cup_{producto.pk}')
            if f'cambio_cup_{producto.pk}' in request.POST:
                producto.cambio_mlc = request.POST.get(f'cambio_mlc_{producto.pk}')
            if f'encargado_{producto.pk}' in request.POST:
                producto.encargado = True
            if f'recibido_{producto.pk}' in request.POST:
                producto.recibido = True
            if f'entregado_{producto.pk}' in request.POST:
                producto.entregado = True
            producto.save()
        return redirect('/clientes/')  # Redirigir después de la actualización

    return render(request, 'facturas/modificar-facturas.html', {
        'productos': productos,
        'fecha':fecha,
        'cliente':cliente,
        })
