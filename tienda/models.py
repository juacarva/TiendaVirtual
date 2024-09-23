from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('tienda:lista_productos', args=[self.slug])

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, related_name='productos', on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    disponible = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, unique=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('tienda:detalle_producto', args=[self.id])

class DireccionEnvio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    pais = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.direccion}, {self.ciudad}, {self.codigo_postal}, {self.pais}"

class Invitado(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class OrdenCompra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    invitado = models.ForeignKey(Invitado, on_delete=models.SET_NULL, null=True, blank=True)
    direccion_envio = models.ForeignKey(DireccionEnvio, on_delete=models.SET_NULL, null=True)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class DetalleOrden(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)



