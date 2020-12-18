# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id_bodega', models.SmallIntegerField(serialize=False, primary_key=True)),
                ('codigo_bodega', models.CharField(max_length=25, null=True, blank=True)),
                ('fecha_materiales', models.DateField(null=True, blank=True)),
                ('fecha_materiales_sobrantes', models.DateField(null=True, blank=True)),
                ('observaciones', models.CharField(max_length=100, null=True, blank=True)),
                ('fecha_recibido_produccion', models.DateField(null=True, blank=True)),
            ],
            options={
                'db_table': 'bodega',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id_categoria', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=5, null=True, blank=True)),
                ('descripcion', models.CharField(max_length=25, null=True, blank=True)),
            ],
            options={
                'db_table': 'categoria',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cheque',
            fields=[
                ('id_cheque', models.SmallIntegerField(serialize=False, primary_key=True)),
                ('fecha_cheque', models.DateField(null=True, blank=True)),
                ('observaciones', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'db_table': 'cheque',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id_cliente', models.SmallIntegerField(serialize=False, primary_key=True)),
                ('nombre_cliente', models.CharField(max_length=75, null=True, blank=True)),
                ('contacto_cliente', models.CharField(max_length=75, null=True, blank=True)),
                ('direccion_cliente', models.CharField(max_length=75, null=True, blank=True)),
                ('telefono_cliente', models.CharField(max_length=50, null=True, blank=True)),
                ('correo_cliente', models.CharField(max_length=75, null=True, blank=True)),
            ],
            options={
                'db_table': 'cliente',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id_control', models.IntegerField(serialize=False, primary_key=True)),
                ('informacion', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'db_table': 'control',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id_factura', models.SmallIntegerField(serialize=False, primary_key=True)),
                ('fecha_factura', models.DateField(null=True, blank=True)),
                ('dato1', models.CharField(max_length=25, null=True, blank=True)),
                ('dato2', models.CharField(max_length=25, null=True, blank=True)),
            ],
            options={
                'db_table': 'factura',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id_historial', models.AutoField(serialize=False, primary_key=True)),
                ('fecha', models.DateField(null=True, blank=True)),
            ],
            options={
                'db_table': 'historial',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NoPedido',
            fields=[
                ('id_pedido', models.SmallIntegerField(serialize=False, primary_key=True)),
                ('descripcion', models.CharField(max_length=175, null=True, blank=True)),
                ('solicitado', models.CharField(max_length=150, null=True, blank=True)),
            ],
            options={
                'db_table': 'no_pedido',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id_orden', models.SmallIntegerField(serialize=False, primary_key=True)),
                ('fecha_orden', models.DateField(null=True, blank=True)),
                ('fecha_produccion', models.DateField(null=True, blank=True)),
                ('fecha_envio', models.DateField(null=True, blank=True)),
                ('direccion_proyecto', models.CharField(max_length=75, null=True, blank=True)),
                ('nombre_encargado', models.CharField(max_length=50, null=True, blank=True)),
                ('instalacion', models.IntegerField(null=True, blank=True)),
                ('cancelado', models.IntegerField(null=True, blank=True)),
                ('fecha_cancelacion', models.DateField(null=True, blank=True)),
                ('fecha_entrega_bodega', models.DateField(null=True, blank=True)),
                ('fecha_entrega_cliente', models.DateField(null=True, blank=True)),
                ('observacion', models.CharField(max_length=200, null=True, blank=True)),
                ('total_metro', models.SmallIntegerField(null=True, blank=True)),
                ('tipo_vidrio', models.CharField(max_length=25, null=True, blank=True)),
            ],
            options={
                'db_table': 'orden',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Orden2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'orden2',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrdenP',
            fields=[
                ('id_orden_p', models.SmallIntegerField(serialize=False, primary_key=True)),
                ('fecha_orden_p', models.DateField(null=True, blank=True)),
                ('fecha_pago', models.DateField(null=True, blank=True)),
                ('descuento', models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True)),
                ('concepto', models.CharField(max_length=75, null=True, blank=True)),
                ('forma_pago', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'db_table': 'orden_p',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.SmallIntegerField(serialize=False, primary_key=True)),
                ('fecha_entrega', models.DateField(null=True, blank=True)),
                ('codigo', models.CharField(max_length=50, null=True, blank=True)),
                ('cantidad', models.SmallIntegerField(null=True, blank=True)),
                ('color', models.CharField(max_length=25, null=True, blank=True)),
                ('funcion', models.CharField(max_length=50, null=True, blank=True)),
                ('medida', models.CharField(max_length=25, null=True, blank=True)),
                ('descripcion', models.CharField(max_length=100, null=True, blank=True)),
                ('precio', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
                ('total', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('revisado_transportista', models.CharField(max_length=50, null=True, blank=True)),
                ('nombre_recibido_proyecto', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'db_table': 'producto',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductoB',
            fields=[
                ('id_productob', models.SmallIntegerField(serialize=False, primary_key=True)),
                ('codigo', models.CharField(max_length=50, null=True, blank=True)),
                ('paquete', models.SmallIntegerField(null=True, blank=True)),
                ('unidad_medida', models.CharField(max_length=25, null=True, blank=True)),
                ('metro_lineal', models.SmallIntegerField(null=True, blank=True)),
                ('tira', models.SmallIntegerField(null=True, blank=True)),
                ('pieza_sobrante', models.SmallIntegerField(null=True, blank=True)),
                ('descripcion', models.CharField(max_length=100, null=True, blank=True)),
                ('total_unidad', models.SmallIntegerField(null=True, blank=True)),
                ('unidad_paquete', models.SmallIntegerField(null=True, blank=True)),
                ('desperdicio', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'db_table': 'producto_b',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductoP',
            fields=[
                ('id_productop', models.SmallIntegerField(serialize=False, primary_key=True)),
                ('noo', models.IntegerField(null=True, blank=True)),
                ('codigo', models.CharField(max_length=25, null=True, blank=True)),
                ('serie', models.CharField(max_length=25, null=True, blank=True)),
                ('descripcion', models.CharField(max_length=100, null=True, blank=True)),
                ('unidad_medida', models.CharField(max_length=25, null=True, blank=True)),
                ('metro_lineal', models.SmallIntegerField(null=True, blank=True)),
                ('tira', models.SmallIntegerField(null=True, blank=True)),
                ('precio', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
                ('precio_descuento', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
                ('total', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
            ],
            options={
                'db_table': 'producto_p',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id_proveedor', models.SmallIntegerField(serialize=False, primary_key=True)),
                ('nombre_proveedor', models.CharField(max_length=75, null=True, blank=True)),
                ('contacto_proveedor', models.CharField(max_length=75, null=True, blank=True)),
                ('direccion_proveedor', models.CharField(max_length=75, null=True, blank=True)),
                ('telefono_proveedor', models.CharField(max_length=50, null=True, blank=True)),
                ('correo_proveedor', models.CharField(max_length=75, null=True, blank=True)),
                ('anexo', models.CharField(max_length=10, null=True, blank=True)),
            ],
            options={
                'db_table': 'proveedor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Prueba',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.IntegerField(null=True, blank=True)),
                ('nombre', models.CharField(max_length=30, null=True, blank=True)),
            ],
            options={
                'db_table': 'prueba',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('nombre_rol', models.CharField(max_length=20, null=True, blank=True)),
            ],
            options={
                'db_table': 'rol',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('codigo', models.AutoField(serialize=False, primary_key=True)),
                ('contrasena', models.CharField(max_length=20)),
                ('nombre_usuario', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'usuario',
                'managed': False,
            },
        ),
    ]
