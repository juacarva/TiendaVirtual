# Generated by Django 5.1.1 on 2024-09-24 12:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0007_alter_categoria_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleorden',
            name='orden',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='tienda.ordencompra'),
        ),
    ]
