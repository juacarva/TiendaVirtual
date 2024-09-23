from django.test import TestCase
from django.urls import reverse
from .models import Producto, Categoria

class ProductoTests(TestCase):

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Categoria 1', slug='categoria-1')
        self.producto = Producto.objects.create(
            nombre='Producto 1',
            categoria=self.categoria,
            descripcion='Descripción del producto 1',
            precio=10.00,
            stock=100,
            disponible=True,
            slug='producto-1'
        )

    def test_lista_productos_view(self):
        response = self.client.get(reverse('tienda:lista_productos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Producto 1')

    def test_detalle_producto_view(self):
        response = self.client.get(reverse('tienda:detalle_producto', args=[self.producto.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Producto 1')
