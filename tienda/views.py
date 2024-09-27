from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria, OrdenCompra, DetalleOrden, DireccionEnvio, Invitado
from .forms import SeleccionarDireccionForm, InvitadoForm, CustomUserCreationForm
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def lista_productos(request, categoria_slug=None):
    categoria = None
    categorias = Categoria.objects.all()
    productos = Producto.objects.filter(disponible=True)
    
    if categoria_slug:
        categoria = get_object_or_404(Categoria, slug=categoria_slug)
        productos = productos.filter(categoria=categoria)
    
    return render(request, 'tienda/lista_productos.html', {
        'categoria': categoria,
        'categorias': categorias,
        'productos': productos
    })

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id, disponible=True)
    return render(request, 'tienda/detalle_producto.html', {'producto': producto})


def agregar_al_carrito(request, id):
    producto = get_object_or_404(Producto, id=id)
    carrito = request.session.get('carrito', {})
    cantidad = int(request.POST.get('cantidad', 1))
    
    if str(id) in carrito:
        nueva_cantidad = carrito[str(id)]['cantidad'] + cantidad
    else:
        nueva_cantidad = cantidad
    
    if nueva_cantidad > producto.stock:
        lmessages.error(request, f"No puedes agregar al carro de compras más de {producto.stock} unidades en total del producto {producto.nombre}.")
        return redirect('tienda:detalle_producto', id=id)
    
    if str(id) in carrito:
        carrito[str(id)]['cantidad'] = nueva_cantidad
    else:
        carrito[str(id)] = {'nombre': producto.nombre, 'precio': str(producto.precio), 'cantidad': cantidad}
    
    request.session['carrito'] = carrito
    messages.success(request, f"{producto.nombre} ha sido agregado al carrito.")
    return redirect('tienda:ver_carrito')

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = sum(float(item['precio']) * item['cantidad'] for item in carrito.values())
    return render(request, 'tienda/ver_carrito.html', {'carrito': carrito, 'total': total})

def eliminar_del_carrito(request, id):
    carrito = request.session.get('carrito', {})
    if str(id) in carrito:
        del carrito[str(id)]
    request.session['carrito'] = carrito
    return redirect('tienda:ver_carrito')

def seleccionar_direccion(request):
    if request.method == 'POST':
        form = SeleccionarDireccionForm(request.POST, user=request.user)
        if form.is_valid():
            direccion = form.save(commit=False)
            if request.user.is_authenticated:
                direccion.usuario = request.user
                direccion.save()
            else:
                # Guardar datos temporales en la sesión para usuarios anónimos
                request.session['direccion'] = form.cleaned_data['direccion']
                request.session['ciudad'] = form.cleaned_data['ciudad']
                request.session['codigo_postal'] = form.cleaned_data['codigo_postal']
                request.session['pais'] = form.cleaned_data['pais']
            request.session['direccion_envio_id'] = direccion.id if request.user.is_authenticated else None
            return redirect('tienda:resumen_compra')
    else:
        form = SeleccionarDireccionForm(user=request.user)
        direcciones = DireccionEnvio.objects.filter(usuario=request.user) if request.user.is_authenticated else []

    return render(request, 'tienda/seleccionar_direccion.html', {'form': form, 'direcciones': direcciones, 'user_authenticated': request.user.is_authenticated})

def seleccionar_direccion_guardada(request, direccion_id):
    if request.user.is_authenticated:
        direccion = get_object_or_404(DireccionEnvio, id=direccion_id, usuario=request.user)
        request.session['direccion_envio_id'] = direccion.id
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def resumen_compra(request):
    carrito = request.session.get('carrito', {})
    direccion_envio_id = request.session.get('direccion_envio_id')
    if request.user.is_authenticated:
        direccion_envio = get_object_or_404(DireccionEnvio, id=direccion_envio_id)
    else:
        direccion_envio = {
            'direccion': request.session.get('direccion'),
            'ciudad': request.session.get('ciudad'),
            'codigo_postal': request.session.get('codigo_postal'),
            'pais': request.session.get('pais'),
            'nombre': request.session.get('nombre'),
            'email': request.session.get('email')
        }
    total = calcular_total_carrito(carrito)
    return render(request, 'tienda/resumen_compra.html', {'carrito': carrito, 'direccion_envio': direccion_envio, 'total': total})



def confirmar_compra(request):
    carrito = request.session.get('carrito', {})
    direccion_envio_id = request.session.get('direccion_envio_id')
    
    if request.user.is_authenticated:
        direccion_envio = get_object_or_404(DireccionEnvio, id=direccion_envio_id)
    else:
        direccion_data = {
            'direccion': request.session.get('direccion'),
            'ciudad': request.session.get('ciudad'),
            'codigo_postal': request.session.get('codigo_postal'),
            'pais': request.session.get('pais'),
        }
        direccion_envio = DireccionEnvio.objects.create(**direccion_data)
    
    total = sum(int(item['cantidad']) * float(item['precio']) for item in carrito.values())
    
    if request.user.is_authenticated:
        usuario = request.user
        invitado = None
    else:
        usuario = None
        email = request.session.get('email')
        try:
            invitado = Invitado.objects.get(email=email)
        except Invitado.DoesNotExist:
            return redirect('tienda:registrar_invitado')
    
    orden = OrdenCompra.objects.create(
        usuario=usuario,
        invitado=invitado,
        direccion_envio=direccion_envio,
        fecha_compra=timezone.now(),
        total=total
    )
    
    for item_id, item in carrito.items():
        producto = get_object_or_404(Producto, id=item_id)
        cantidad = int(item['cantidad'])
        DetalleOrden.objects.create(
            orden=orden,
            producto=producto,
            cantidad=cantidad,
            precio=float(item['precio'])
        )
        # Actualizar el stock del producto
        producto.stock -= cantidad
        producto.save()
    
    request.session['carrito'] = {}
    
    # Enviar correo electrónico de confirmación
    subject = 'Confirmación de tu orden de compra'
    html_message = render_to_string('tienda/email_orden.html', {'orden': orden})
    plain_message = strip_tags(html_message)
    from_email = 'tu_email@gmail.com'
    to = [usuario.email if usuario else invitado.email]
    
    send_mail(subject, plain_message, from_email, to, html_message=html_message)
    
    return render(request, 'tienda/confirmacion_compra.html', {'orden': orden})


def calcular_total_carrito(carrito):
    return sum(float(item['precio']) * item['cantidad'] for item in carrito.values())


def registrar_invitado(request):
    if request.method == 'POST':
        form = InvitadoForm(request.POST)
        if form.is_valid():
            invitado = form.save()
            request.session['email'] = invitado.email
            return redirect('tienda:seleccionar_direccion')
    else:
        form = InvitadoForm()
    return render(request, 'tienda/registrar_invitado.html', {'form': form})

def seleccionar_opcion_compra(request):
    if request.method == 'POST':
        if 'registrarse' in request.POST:
            return redirect('tienda:registrar_usuario')
        elif 'comprar_como_invitado' in request.POST:
            return redirect('tienda:registrar_invitado')
        elif 'iniciar_sesion' in request.POST:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('tienda:seleccionar_direccion')
    else:
        form = AuthenticationForm()
    return render(request, 'tienda/seleccionar_opcion_compra.html', {'form': form})


def registrar_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tienda:lista_productos')
    else:
        form = CustomUserCreationForm()
    return render(request, 'tienda/registrar_usuario.html', {'form': form})

def descargar_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, id=orden_id)
    template_path = 'tienda/orden_pdf.html'
    context = {'orden': orden}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="orden_{orden.id}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF: %s' % pisa_status.err, status=400)
    
    return response

def confirmacion_compra(request, orden_id):
    orden = get_object_or_404(OrdenCompra, id=orden_id)
    return render(request, 'tienda/confirmacion_compra.html', {'orden': orden})