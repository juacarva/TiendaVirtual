from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'tienda'

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('categoria/<slug:categoria_slug>/', views.lista_productos, name='lista_productos_por_categoria'),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('seleccionar-opcion-compra/', views.seleccionar_opcion_compra, name='seleccionar_opcion_compra'),
    path('registrar-usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('registrar-invitado/', views.registrar_invitado, name='registrar_invitado'),  # Asegúrate de que esta línea esté presente
    path('seleccionar_direccion/', views.seleccionar_direccion, name='seleccionar_direccion'),
    path('seleccionar_direccion/<int:direccion_id>/', views.seleccionar_direccion_guardada, name='seleccionar_direccion_guardada'),
    path('resumen-compra/', views.resumen_compra, name='resumen_compra'),
    path('confirmar-compra/', views.confirmar_compra, name='confirmar_compra'),
    path('confirmacion-compra/<int:orden_id>/', views.confirmacion_compra, name='confirmacion_compra'),
    path('descargar-orden/<int:orden_id>/', views.descargar_orden, name='descargar_orden'),
    path('login/', auth_views.LoginView.as_view(template_name='tienda/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]