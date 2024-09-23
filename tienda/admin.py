from django.contrib import admin
from .models import Categoria, Producto, OrdenCompra, DetalleOrden

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(OrdenCompra)
admin.site.register(DetalleOrden)
