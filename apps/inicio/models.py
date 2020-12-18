# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Bodega(models.Model):
    id_bodega = models.SmallIntegerField(primary_key=True)
    codigo_bodega = models.CharField(max_length=25, blank=True, null=True)
    fecha_materiales = models.DateField(blank=True, null=True)
    fecha_materiales_sobrantes = models.DateField(blank=True, null=True)
    observaciones = models.CharField(max_length=100, blank=True, null=True)
    cod_orden = models.ForeignKey('Orden', db_column='cod_orden', blank=True, null=True)
    cod_no_id_pedido = models.ForeignKey('NoPedido', db_column='cod_no_id_pedido', blank=True, null=True)
    fecha_recibido_produccion = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bodega'


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        managed = False
        db_table = 'categoria'


class Cheque(models.Model):
    id_cheque = models.SmallIntegerField(primary_key=True)
    fecha_cheque = models.DateField(blank=True, null=True)
    observaciones = models.CharField(max_length=100, blank=True, null=True)
    cod_ordenp = models.ForeignKey('OrdenP', db_column='cod_ordenp', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cheque'


class Cliente(models.Model):
    id_cliente = models.SmallIntegerField(primary_key=True)
    nombre_cliente = models.CharField(max_length=75, blank=True, null=True)
    contacto_cliente = models.CharField(max_length=75, blank=True, null=True)
    direccion_cliente = models.CharField(max_length=75, blank=True, null=True)
    telefono_cliente = models.CharField(max_length=50, blank=True, null=True)
    correo_cliente = models.CharField(max_length=75, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente'


class Control(models.Model):
    id_control = models.IntegerField(primary_key=True)
    informacion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'control'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Factura(models.Model):
    id_factura = models.SmallIntegerField(primary_key=True)
    fecha_factura = models.DateField(blank=True, null=True)
    dato1 = models.CharField(max_length=25, blank=True, null=True)
    dato2 = models.CharField(max_length=25, blank=True, null=True)
    cod_orden = models.ForeignKey('Orden', db_column='cod_orden', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'factura'


class Historial(models.Model):
    id_historial = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    cod_orden = models.ForeignKey('Orden', db_column='cod_orden', blank=True, null=True)
    cod_ordenp = models.ForeignKey('OrdenP', db_column='cod_ordenp', blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historial'


class NoPedido(models.Model):
    id_pedido = models.SmallIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=175, blank=True, null=True)
    solicitado = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'no_pedido'


class Proveedor(models.Model):
    id_proveedor = models.SmallIntegerField(primary_key=True)
    nombre_proveedor = models.CharField(max_length=75, blank=True, null=True)
    contacto_proveedor = models.CharField(max_length=75, blank=True, null=True)
    direccion_proveedor = models.CharField(max_length=75, blank=True, null=True)
    telefono_proveedor = models.CharField(max_length=50, blank=True, null=True)
    correo_proveedor = models.CharField(max_length=75, blank=True, null=True)
    anexo = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proveedor'


class Orden(models.Model):
    id_orden = models.SmallIntegerField(primary_key=True)
    serie_orden = models.ForeignKey(Categoria, db_column='serie_orden', blank=True, null=True, default=1)
    fecha_orden = models.DateField(blank=True, null=True)
    fecha_produccion = models.DateField(blank=True, null=True)
    fecha_envio = models.DateField(blank=True, null=True)
    direccion_proyecto = models.CharField(max_length=75, blank=True, null=True)
    nombre_encargado = models.CharField(max_length=50, blank=True, null=True)
    instalacion = models.ForeignKey('Seleccion', db_column='instalacion', blank=True, null=True,default=0)
    cancelado = models.ForeignKey('Seleccion2', db_column='cancelado', blank=True, null=True, default=0)
    tipo_info = models.ForeignKey(Control, db_column='tipo_info', blank=True, null=True)
    no_id_pedido = models.ForeignKey(NoPedido, db_column='no_id_pedido', blank=True, null=True)
    cod_proveedor = models.ForeignKey('Proveedor', db_column='cod_proveedor', blank=True, null=True)
    cod_cliente = models.ForeignKey(Cliente, db_column='cod_cliente', blank=True, null=True)
    cod_vendedor = models.ForeignKey('Usuario', db_column='cod_vendedor', blank=True, null=True)
    fecha_cancelacion = models.DateField(blank=True, null=True)
    fecha_entrega_bodega = models.DateField(blank=True, null=True)
    fecha_entrega_cliente = models.DateField(blank=True, null=True)
    observacion = models.CharField(max_length=200, blank=True, null=True)
    total_metro = models.SmallIntegerField(blank=True, null=True)
    tipo_vidrio = models.CharField(max_length=25, blank=True, null=True)
    fecha_entrega = models.DateField(blank=True, null=True)
    fecha_entrega_produccion = models.DateField(blank=True, null=True)
    fecha_facturacion = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orden'


class OrdenP(models.Model):
    id_orden_p = models.SmallIntegerField(primary_key=True)
    fecha_orden_p = models.DateField(blank=True, null=True)
    fecha_pago = models.DateField(blank=True, null=True)
    descuento = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    concepto = models.CharField(max_length=75, blank=True, null=True)
    forma_pago = models.CharField(max_length=50, blank=True, null=True)
    cod_orden = models.ForeignKey(Orden, db_column='cod_orden', blank=True, null=True)
    cod_proveedor = models.ForeignKey('Proveedor', db_column='cod_proveedor', blank=True, null=True)
    no_id_pedido = models.ForeignKey(NoPedido, db_column='no_id_pedido', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orden_p'


class Producto(models.Model):
    id_producto = models.SmallIntegerField(primary_key=True)
    codigo = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.SmallIntegerField(blank=True, null=True)
    color = models.CharField(max_length=25, blank=True, null=True)
    funcion = models.CharField(max_length=50, blank=True, null=True)
    medida = models.CharField(max_length=25, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    precio = models.DecimalField(max_digits=7, decimal_places=2, default=0.01, blank=True, null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0.01, blank=True, null=True)
    revisado_transportista = models.CharField(max_length=50, blank=True, null=True)
    nombre_recibido_proyecto = models.CharField(max_length=50, blank=True, null=True)
    cod_orden = models.ForeignKey(Orden, db_column='cod_orden', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'producto'


class ProductoB(models.Model):
    id_productob = models.SmallIntegerField(primary_key=True)
    codigo = models.CharField(max_length=50, blank=True, null=True)
    paquete = models.SmallIntegerField(blank=True, null=True)
    unidad_medida = models.CharField(max_length=25, blank=True, null=True)
    metro_lineal = models.SmallIntegerField(blank=True, null=True)
    tira = models.SmallIntegerField(blank=True, null=True)
    pieza_sobrante = models.SmallIntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    total_unidad = models.SmallIntegerField(blank=True, null=True)
    unidad_paquete = models.SmallIntegerField(blank=True, null=True)
    desperdicio = models.CharField(max_length=100, blank=True, null=True)
    cod_bodega = models.ForeignKey(Bodega, db_column='cod_bodega', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'producto_b'


class ProductoP(models.Model):
    id_productop = models.SmallIntegerField(primary_key=True)
    noo = models.IntegerField(blank=True, null=True)
    codigo = models.CharField(max_length=25, blank=True, null=True)
    serie = models.CharField(max_length=25, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    unidad_medida = models.CharField(max_length=25, blank=True, null=True)
    metro_lineal = models.SmallIntegerField(blank=True, null=True)
    tira = models.SmallIntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    precio_descuento = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    cod_ordenp = models.ForeignKey(OrdenP, db_column='cod_ordenp', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'producto_p'


class Prueba(models.Model):
    codigo = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prueba'


class Rol(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre_rol = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nombre_rol)

    class Meta:
        managed = False
        db_table = 'rol'


class Seleccion(models.Model):
    id_seleccion = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        managed = False
        db_table = 'seleccion'


class Seleccion2(models.Model):
    id_seleccion = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        managed = False
        db_table = 'seleccion2'


class Usuario(models.Model):
    codigo = models.AutoField(primary_key=True)
    contrasena = models.CharField(max_length=20)
    nombre_usuario = models.CharField(max_length=30)
    tipo_rol = models.ForeignKey(Rol, db_column='tipo_rol', default=0)

    class Meta:
        managed = False
        db_table = 'usuario'
