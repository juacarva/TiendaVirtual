# Generated by Django 5.1.1 on 2024-09-17 13:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0004_remove_ordenitem_orden_remove_ordenitem_producto_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='detalleorden',
            name='orden',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.ordencompra'),
        ),
        migrations.AlterField(
            model_name='ordencompra',
            name='direccion_envio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tienda.direccionenvio'),
        ),
        migrations.AlterField(
            model_name='ordencompra',
            name='fecha_compra',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ordencompra',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ordencompra',
            name='invitado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tienda.invitado'),
        ),
    ]
