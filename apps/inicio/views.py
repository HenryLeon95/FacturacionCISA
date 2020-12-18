# -*- coding: utf-8 -*-
from datetime import *

from django.core.paginator import Paginator
from django.db.models import F
import math
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics
from apps.inicio.serializers import *
from django.db import connection
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View
from apps.inicio.forms import *
from apps.inicio.models import *
from django.contrib import messages
from django.db.models import Sum
from django.core import serializers
from django.conf import settings
from io import BytesIO
import io
from reportlab.pdfgen import canvas
from django.http import FileResponse

from reportlab.lib.units import cm
from reportlab.platypus import Table, Paragraph, SimpleDocTemplate, Image, Spacer
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter


# Create your views here.


def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        datos = form.cleaned_data
        nombre_usuario = datos.get("nombre_usuario")
        contrasena = datos.get("contrasena")
        tipo_rol = datos.get("tipo_rol")
        print (contrasena)
        try:
            acceso = Usuario.objects.get(nombre_usuario=nombre_usuario, contrasena=contrasena)
            print (acceso.tipo_rol.id)
            try:
                tipo_rol = acceso.tipo_rol.id
                cc = acceso.codigo
                request.session['codigo'] = cc
            except TypeError:
                print ("Error")
        except Usuario.DoesNotExist:
            acceso = None
        if acceso:
            messages.success(request, "Bienvenido {}".format(nombre_usuario))
            if tipo_rol == 1:
                print ("Si Administrador")
                return redirect('ventas:admon')
            elif tipo_rol == 2:
                print ("Si Vendedor")
                return redirect('ventas:admon')
            elif tipo_rol == 3:
                print ("Si Facturador")
                return redirect('ventas:admon')
            elif tipo_rol == 4:
                print ("Si Coordinador")
                return redirect('ventas:admon')
            else:
                print ("Nada")
                return HttpResponseRedirect('/404Not/')
        else:
            messages.success(request, "Credenciales incorrectas")
    else:
        form = LoginForm()

    var = {
        "form_login":form,
    }
    return render(request, 'base/login.html', var)


def my_login_required(function):
    def wrapper(request, *args, **kw):
        if not (request.session.get('codigo')):
            print ("Not")
            return HttpResponseRedirect('/404Not/')
        else:
            print ("Yes")
            return function(request, *args, **kw)
    return wrapper


def error(request):
    return render(request,'base/error.html')


def error2(request):
    return render(request,'base/error2.html')


class UserList(ListView):
    model = Usuario
    template_name = 'base/base.html'


class OrdenList(ListView):
    model = Orden
    template_name = 'orden_general/orden_form.html'
    paginate_by = 8


def OrdenDetalle(request, pk):
    orden = Orden.objects.get(id_orden = pk)
    proveedor = Proveedor.objects.get(id_proveedor=orden.cod_proveedor.id_proveedor)
    cliente = Cliente.objects.get(id_cliente = orden.cod_cliente.id_cliente)
    pedido = NoPedido.objects.get(id_pedido = orden.no_id_pedido.id_pedido)
    producto = Producto.objects.filter(cod_orden =pk)
    total = precio = 0
    #total = producto.aggregate(Sum('total'))
    for key in producto:
        try:
            total = total +key.total
        except:
            print (".")
    #precio= producto.aggregate( precio = Sum(F('total') * F('total')))['precio']
    #print (type(total))
    try:
        precio = total / orden.total_metro
    except:
        print ("..")
    if request.method == 'GET':
        form = OrdenForm(instance=orden)
        form2 = ProveedorForm(instance=proveedor)
        form3 = ClienteForm(instance=cliente)
        form4 = NoPedidoForm(instance=pedido)
    return render(request, 'orden_general/orden_producto_form.html',{'form':form, 'form2':form2, 'form3':form3, 'form4':form4,
                                                                     'resultado':producto, 'total':total, 'precio':precio})


def MyOrden(request,valor):
    if valor == 0 or valor == "0":
        hh = request.session.get('codigo')
        orden = Orden.objects.filter(cod_vendedor=hh, tipo_info=valor)
        pag = Paginate(request,orden,8)
        # Contexto a retornar a la vista
        cxt = {
            'posts': pag['queryset'],
            'totPost': orden,
            'paginator': pag
        }
    elif valor ==1 or valor == "1":
        hh = request.session.get('codigo')
        orden1 = Orden.objects.filter(cod_vendedor=hh, tipo_info=valor)
        orden2 = Orden.objects.filter(cod_vendedor=hh, tipo_info=2)
        pag1 = Paginate(request, orden1, 8)
        pag2 = Paginate(request, orden2, 8)
        # Contexto a retornar a la vista
        cxt = {
            'posts1': pag1['queryset'], 'posts2': pag2['queryset'],
            'totPost1': orden1, 'totPost2': orden2,
            'paginator1': pag1,'paginator2': pag2
        }
    elif valor ==3 or valor == "3":
        hh = request.session.get('codigo')
        orden3 = Orden.objects.filter(cod_vendedor=hh, tipo_info=valor)
        orden4 = Orden.objects.filter(cod_vendedor=hh, tipo_info=4)
        pag3 = Paginate(request, orden3, 8)
        pag4 = Paginate(request, orden4, 8)
        # Contexto a retornar a la vista
        cxt = {
            'posts3': pag3['queryset'], 'posts4': pag4['queryset'],
            'totPost3': orden3, 'totPost4': orden4,
            'paginator3': pag3,'paginator4': pag4
        }
    elif valor ==5 or valor == "5":
        hh = request.session.get('codigo')
        orden5 = Orden.objects.filter(cod_vendedor=hh, tipo_info=valor)
        orden11 = Orden.objects.filter(cod_vendedor=hh, tipo_info=11)
        orden12 = Orden.objects.filter(cancelado=1)
        pag5 = Paginate(request, orden5, 8)
        pag11 = Paginate(request, orden11, 8)
        pag12 = Paginate(request, orden12, 8)
        # Contexto a retornar a la vista
        cxt = {
            'posts5': pag5['queryset'], 'posts11': pag11['queryset'], 'posts12': pag12['queryset'],
            'totPost5': orden5, 'totPost11': orden11, 'totPost12': orden12,
            'paginator5': pag5, 'paginator11': pag11, 'paginator12': pag12
        }
    else:
        hh = request.session.get('codigo')
        orden = Orden.objects.filter(cod_vendedor=hh, tipo_info=valor)
        pag = Paginate(request, orden, 8)
        # Contexto a retornar a la vista
        cxt = {
            'posts': pag['queryset'],
            'totPost': orden,
            'paginator': pag
        }
    return render_to_response('orden_general/mis_ordenes.html', context_instance=RequestContext(request, cxt))


def Busqueda(request, id, valor):
    if id == 201503577 or id == "201503577":
        #Toddas la O.P (Solo para el Administrador y coordinador)
        if valor == 201503578 or valor == "201503578":
            orden1 = Orden.objects.filter(tipo_info=1)
            orden2 = Orden.objects.filter(tipo_info=2)
            pag1 = Paginate(request, orden1, 8)
            pag2 = Paginate(request, orden2, 8)
            cxt = {
                'posts1': pag1['queryset'], 'posts2': pag2['queryset'],
                'paginator1': pag1, 'paginator2': pag2,
                'bandera': id,
            }

            #Para ordenar(crear) las O.P
        elif valor == 201503579 or valor == "201503579":
            orden1 = Orden.objects.filter(tipo_info=1)
            pag1 = Paginate(request, orden1, 8)
            cxt = {
                'posts1': pag1['queryset'],
                'paginator1': pag1,
                'bandera': id,
            }
            return render_to_response('produccion/produccion_select.html', context_instance=RequestContext(request, cxt))

            # Toddas la O.P (Solo para el Administrador y coordinador)
        elif valor == 201503580 or valor == "201503580":
            orden3 = Orden.objects.filter(tipo_info=3)
            orden4 = Orden.objects.filter(tipo_info=4)
            pag3 = Paginate(request, orden3, 8)
            pag4 = Paginate(request, orden4, 8)
            cxt = {
                'posts3': pag3['queryset'], 'posts4': pag4['queryset'],
                'paginator3': pag3, 'paginator4': pag4,
                'bandera': id,
            }

            # Toddas la Facturas (Solo para el Administrador)
        elif valor == 201503581 or valor == "201503581":
            orden5 = Orden.objects.filter(tipo_info=5)
            orden11 = Orden.objects.filter(tipo_info=11)
            orden12 = Orden.objects.filter(cancelado=1)
            pag5 = Paginate(request, orden5, 8)
            pag11 = Paginate(request, orden11, 8)
            pag12 = Paginate(request, orden12, 8)
            cxt = {
                'posts5': pag5['queryset'], 'posts11': pag11['queryset'], 'posts12': pag12['queryset'],
                'paginator5': pag5, 'paginator11': pag11, 'paginator12': pag12,
                'bandera': id,
            }

            #Todas las O.C
        else:
            orden = Orden.objects.filter(tipo_info=valor)
            pag = Paginate(request, orden, 8)
            if valor == 0 or valor == "0":  # Orden de Compras
                orden10 = Orden.objects.filter(tipo_info=10)
                pag10 = Paginate(request, orden10, 8)
                cxt = {'posts': pag['queryset'], 'posts10': pag10['queryset'], 'totPost': orden, 'totPost10': orden10,
                       'paginator': pag, 'paginator10': pag10, 'bandera': id, }
            elif valor == 1 or valor == "1":  # En O.P
                cxt = {'posts': pag['queryset'], 'totPost': orden, 'paginator': pag, 'bandera1': id, }
            elif valor == 2 or valor == "2":  # Produccion Finalizada
                cxt = {'posts': pag['queryset'], 'totPost': orden, 'paginator': pag, 'bandera2': id, }
            elif valor == 3 or valor == "3":  # En Envio
                cxt = {'posts': pag['queryset'], 'totPost': orden, 'paginator': pag, 'bandera3': id, }
            elif valor == 4 or valor == "4":  # Envio Finalizado
                cxt = {'posts': pag['queryset'], 'totPost': orden, 'paginator': pag, 'bandera4': id, }
            elif valor == 5 or valor == "5":  # ya Facturado
                cxt = {'posts': pag['queryset'], 'totPost': orden, 'paginator': pag, 'bandera5': id, }
            elif valor == 10 or valor == "10":  # Orden Anulada
                cxt = {'posts': pag['queryset'], 'totPost': orden, 'paginator': pag, 'bandera10': id, }
            else:  # Factura Impresa Incorrectamente
                cxt = {'posts': pag['queryset'], 'totPost': orden, 'paginator': pag, 'bandera11': id, }

        # Ver Ordenes
    elif valor == 201503577 or valor == "201503577":
        orden = Orden.objects.filter(cod_vendedor=id, tipo_info=0)
        orden1 = Orden.objects.filter(cod_vendedor=id, tipo_info=1)
        orden2 = Orden.objects.filter(cod_vendedor=id, tipo_info=2)
        orden3 = Orden.objects.filter(cod_vendedor=id, tipo_info=3)
        orden4 = Orden.objects.filter(cod_vendedor=id, tipo_info=4)
        orden5 = Orden.objects.filter(cod_vendedor=id, tipo_info=5)
        orden10 = Orden.objects.filter(cod_vendedor=id, tipo_info=10)
        orden11 = Orden.objects.filter(cod_vendedor=id, tipo_info=11)
        orden12 = Orden.objects.filter(cod_vendedor=id, cancelado=1)
        pag = Paginate(request, orden, 8)
        pag1 = Paginate(request, orden1, 8)
        pag2 = Paginate(request, orden2, 8)
        pag3 = Paginate(request, orden3, 8)
        pag4 = Paginate(request, orden4, 8)
        pag5 = Paginate(request, orden5, 8)
        pag10 = Paginate(request, orden10, 8)
        pag11 = Paginate(request, orden11, 8)
        pag12 = Paginate(request, orden12, 8)
        # Contexto a retornar a la vista
        cxt = {
            'posts': pag['queryset'], 'posts1': pag1['queryset'], 'posts2': pag2['queryset'], 'posts3': pag3['queryset'],
            'posts4': pag4['queryset'], 'posts5': pag5['queryset'], 'posts10': pag10['queryset'], 'posts11': pag11['queryset'], 'posts12': pag12['queryset'],
            'totPost': orden,
            'paginator': pag, 'paginator1': pag1, 'paginator2': pag2, 'paginator3': pag3, 'paginator4': pag4, 'paginator5': pag5,
            'paginator10': pag10, 'paginator11': pag11, 'paginator12': pag12,
            'bandera': id,
        }

    else:
        orden = Orden.objects.filter(cod_vendedor=id, tipo_info=valor)
        pag = Paginate(request, orden, 8)
        if valor == 0 or valor == "0":                                  #Orden de Compras
            cxt = {'posts': pag['queryset'], 'totPost': orden, 'paginator': pag, 'bandera': id, }
        elif valor == 1 or valor == "1":                                #En O.P
            cxt = {'posts': pag['queryset'], 'totPost': orden, 'paginator': pag, 'bandera1': id, }
        elif valor == 2 or valor == "2":                                #Produccion finalizada
            cxt = {'posts': pag['queryset'], 'totPost': orden, 'paginator': pag, 'bandera2': id, }
        elif valor == 3 or valor == "3":                                #En O.E
            cxt = {'posts': pag['queryset'], 'totPost': orden, 'paginator': pag, 'bandera3': id, }
        elif valor == 4 or valor == "4":                                #O.E Finalizado
            cxt = {'posts': pag['queryset'], 'totPost': orden, 'paginator': pag, 'bandera4': id, }
        elif valor == 5 or valor == "5":                                #Ya Facturado
            cxt = {'posts': pag['queryset'], 'totPost': orden, 'paginator': pag, 'bandera5': id, }
        elif valor == 10 or valor == "10":                                #Anulado
            cxt = {'posts': pag['queryset'], 'totPost': orden, 'paginator': pag, 'bandera10': id, }
        else:                                #Factura impresa incorrectamente
            cxt = {'posts': pag['queryset'], 'totPost': orden, 'paginator': pag, 'bandera11': id, }

    return render_to_response('orden_general/mis_ordenes.html', context_instance=RequestContext(request, cxt))

"""
Para Paginar Paginas usando Funciones
PARAMETROS:
request: Request de la vista
queryset: Queryset a utilizar en la paginacion
"""


def Paginate(request, queryset, pages):
    # Retorna el objeto paginator para comenzar el trabajo
    result_list = Paginator(queryset, pages)

    try:
        # Tomamos el valor de parametro page, usando GET
        page = int(request.GET.get('page'))
    except:
        page = 1

    # Si es menor o igual a 0 igualo en 1
    if page <= 0:
        page = 1

    # Si viene un parametro que es mayor a la cantidad
    # de paginas le igualo el parametro con las cant de paginas
    if (page > result_list.num_pages):
        page = result_list.num_pages

    # Verificamos si esta dentro del rango
    if (result_list.num_pages >= page):
        # Obtengo el listado correspondiente al page
        pagina = result_list.page(page)

        context = {
            'queryset': pagina.object_list,
            'page': page,
            'pages': result_list.num_pages,
            'has_next': pagina.has_next(),
            'has_prev': pagina.has_previous(),
            'next_page': page + 1,
            'prev_page': page - 1,
            'firstPage': 1,
        }
    return context


"""
Para poder devolver el contenido en formato JSON
"""


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def prueba_list(request):
    if request.method == 'GET':
        pruebas = Prueba.objects.all()
        serializer = Prueba1Serializer(pruebas, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Prueba1Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def prueba_detail(request, pk):
    try:
        prueba = Prueba.objects.get(pk=pk)
    except Prueba.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = Prueba1Serializer(prueba)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = Prueba1Serializer(prueba, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        prueba.delete()
        return HttpResponse(status=204)


class Prueba2List(generics.ListCreateAPIView):
    queryset = Prueba.objects.all()
    serializer_class = Prueba2Serializer


class Prueba2Detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prueba.objects.all()
    serializer_class = Prueba2Serializer


class UsuarioCreate(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'base/usuario_form.html'
    success_url = reverse_lazy('ventas:admon')


class UsuarioEliminar(DeleteView):
     model = Usuario
     template_name = 'base/usuario_delete.html'
     success_url = reverse_lazy('ventas:admon')


class UsuarioUpdate(UpdateView):
        model = Usuario
    form_class = UsuarioForm2
    template_name = 'base/usuario_form.html'
    success_url = reverse_lazy('ventas:admon')


def UsuarioDelete(request,codigo):
    usuario = Usuario.objects.get(codigo=codigo)
    if request.method == 'POST':
        usuario.delete()
        return redirect('ventas:admon')
    return render(request, 'base/usuario_delete.html', {'usuario':usuario})


class OrdenCreate(CreateView):
    model = Orden
    template_name = 'orden_general/producto_form.html'
    form_class = OrdenForm
    second_form_class = ProveedorForm
    third_form_class = ClienteForm
    quarter_form_class = NoPedidoForm
    success_url = reverse_lazy('ventas:admon')

    def get_context_data(self, **kwargs):
        context = super(OrdenCreate, self).get_context_data(**kwargs)
        #Primer Formulario
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        if 'form3' not in context:
            context['form3'] = self.third_form_class(self.request.GET)
        if 'form4' not in context:
            context['form4'] = self.quarter_form_class(self.request.GET)
        context['formset'] = ProductoFormset(queryset=Producto.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        formset = ProductoFormset(request.POST)
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        form3 = self.third_form_class(request.POST)
        form4 = self.quarter_form_class(request.POST)
        if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and formset.is_valid():
            #Coomit = False, Guardara hasta que se guarde los valores del segundo formulario
            print ("antes")
            orden = form.save(commit=False)


            form2.save()
            nuevo = Proveedor.objects.last()
            nuevo.pk = Proveedor.objects.last()
            orden.cod_proveedor = nuevo.id_proveedor

            form3.save()
            nuevo2 = Cliente.objects.last()
            nuevo2.pk = Cliente.objects.last()
            orden.cod_cliente = nuevo2.id_cliente

            form4.save()
            nuevo3 = NoPedido.objects.last()
            nuevo3.pk = NoPedido.objects.last()
            orden.no_id_pedido = nuevo3.id_pedido

            day = datetime.now()
            orden.fecha_orden = day

            pruebacontrol = Control.objects.get(id_control = 0)
            pruebacontrol.pk = Control.objects.get(id_control = 0)
            orden.tipo_info = pruebacontrol.id_control

            hh = request.session.get('codigo')
            pruebavendedor = Usuario.objects.get(codigo = hh)
            pruebavendedor.pk = Usuario.objects.get(codigo = hh)
            orden.cod_vendedor =pruebavendedor.codigo

            try:
                if form.instance.instalacion.id_seleccion == 1 or form.instance.instalacion.id_seleccion == 0:
                    print ("Si selecciono algo")
            except:
                controlorden = Seleccion.objects.get(id_seleccion = 0)
                controlorden.pk = Seleccion.objects.get(id_seleccion = 0)
                orden.instalacion = controlorden.id_seleccion

            try:
                if form.instance.cancelado.id_seleccion == 1 or form.instance.cancelado.id_seleccion == 0:
                    print ("Si selecciono algo")
            except:
                controlorden = Seleccion2.objects.get(id_seleccion=0)
                controlorden.pk = Seleccion2.objects.get(id_seleccion=0)
                orden.cancelado = controlorden.id_seleccion

            try:
                if form.instance.serie_orden.id_categoria == 1 or form.instance.serie_orden.id_categoria == 2 \
                        or form.instance.serie_orden.id_categoria == 3 or form.instance.serie_orden.id_categoria == 4:
                    print ("Si selecciono algo")
            except:
                controlorden = Categoria.objects.get(id_categoria=1)
                controlorden.pk = Categoria.objects.get(id_categoria=1)
                orden.serie_orden = controlorden.id_categoria

            orden.save()
            po = Orden.objects.last()
            po.pk = Orden.objects.last()

            for form5 in formset:
                producto = form5.save(commit=False)
                producto.cod_orden = po.id_orden
                producto.save()

            return HttpResponseRedirect(self.get_success_url())
        else:
            print ("No")
            messages.success(request, "Campos Incorrectos, Verifique tipos y fecha en formato Year-Month-Day")

            return self.render_to_response(self.get_context_data(form = form, form2= form2, form3 = form3, form4= form4, formset = formset))


def Cambiar_Orden(request,cod_orden,valor):
    orden = Orden.objects.get(id_orden=cod_orden)
    if request.method == 'GET':
        if valor != 6 and valor != "6":
            pruebacontrol = Control.objects.get(id_control=valor)
            pruebacontrol.pk = Control.objects.get(id_control=valor)
            orden.tipo_info = pruebacontrol.id_control

        if valor == 3 or valor == "3":
            day = datetime.now()
            orden.fecha_envio = day
        elif valor == 5 or valor == "5":
            day = datetime.now()
            orden.fecha_facturacion = day
        elif valor == 6 or valor == "6":
            day = datetime.now()
            orden.fecha_cancelacion = day

            controlorden = Seleccion2.objects.get(id_seleccion=1)
            controlorden.pk = Seleccion2.objects.get(id_seleccion=1)
            orden.cancelado = controlorden.id_seleccion
            print("Si guardo fecha de cancelacion")
        orden.save()
        print ("Si guardo")
    return redirect('ventas:mi_orden', 0)


def OpCreate(request, pk, valor):
    orden = Orden.objects.get(id_orden = pk)
    proveedor = Proveedor.objects.get(id_proveedor=orden.cod_proveedor.id_proveedor)
    cliente = Cliente.objects.get(id_cliente = orden.cod_cliente.id_cliente)
    pedido = NoPedido.objects.get(id_pedido = orden.no_id_pedido.id_pedido)
    producto = Producto.objects.filter(cod_orden =pk)
    total = precio = 0
    for key in producto:
        try:
            total = total +key.total
        except:
            print (".")
    try:
        precio = total / orden.total_metro
    except:
        print ("..")
    if valor == "1" or valor == 1:  # Crear OP
        if request.method == 'GET':
            form = OrdenForm(instance=orden)
            form2 = ProveedorForm(instance=proveedor)
            form3 = ClienteForm(instance=cliente)
            form4 = NoPedidoForm(instance=pedido)
        elif request.method == 'POST':
            #form = OrdenForm(instance=orden)
            form = OrdenForm(request.POST, instance=orden)
            if form.is_valid():
                day = datetime.now()
                orden.fecha_produccion = day
                orden.save()
            return redirect('ventas:admon')
        return render(request, 'produccion/produccion_form.html',
                      {'form': form, 'form2': form2, 'form3': form3, 'form4': form4,
                       'resultado': producto, 'total': total, 'precio': precio, 'banderaOP': 1})
    else:
        if request.method == 'GET':
            form = OrdenForm(instance=orden)
            form2 = ProveedorForm(instance=proveedor)
            form3 = ClienteForm(instance=cliente)
            form4 = NoPedidoForm(instance=pedido)
    return render(request, 'produccion/produccion_form.html',{'form':form, 'form2':form2, 'form3':form3, 'form4':form4,
                                                                     'resultado':producto, 'total':total, 'precio':precio, 'banderaOP':0})


class ReporteOrdenPDF(View):
    def cabecera(self,pdf,cod_orden,valor):
        from reportlab.lib.units import inch
        from reportlab.lib.colors import HexColor
        PAGE_WIDTH = letter[0]
        PAGE_HEIGHT = letter[1]

        if valor == "0":
                #Ingresamos la imgen
            archivo_imagen = settings.MEDIA_ROOT+'/imagenes/emoji.png'
                # Definimos el tamano de la imagen a cargar y las coordenadas correspondientes
            pdf.drawImage(archivo_imagen, 20, 760, 100, 60, preserveAspectRatio=True)
            #imagen = Image(archivo_imagen, width=100, height=60)
            #imagen.hAlign = 'LEFT'
            #estructura.append(Spacer(20,10))
            #estructura.append(imagen)
                # Establecemos el tamano de letra en 16 y el tipo de letra Helvetica
            pdf.setFont("Helvetica", 13)
                # Dibujamos una cadena en la ubicacion X,Y especificada
            pdf.drawString(130, 815, u"CERRADURAS INTERNACIONALES")
            pdf.setFont("Helvetica", 11)
            pdf.drawString(130, 800, u"Av. Centroamerica 21-51 Z.1")
            pdf.drawString(130, 785, u"Ciudad de Guatemala, Guatemala.")
            pdf.drawString(130,770, u"(+502) 2323-8723")
            pdf.setFont("Helvetica", 11)
            pdf.drawString(375, 800, u"Orden de Compra:")
            serie = Orden.objects.get(id_orden = cod_orden)
            #pdf.setFillColorRGB(0,0.35,0.35)
            pdf.drawString(500, 800, serie.serie_orden.nombre + " -")
            pdf.drawString(515, 800," " + cod_orden)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(375, 785, u"Fecha de O.C:")
            #pdf.setFillColorRGB(0,0.35,0.35)
            pdf.drawString(500, 785, str(serie.fecha_orden.strftime("%d/%m/%Y")))
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(375, 770, u"¿Inclueye instalación?:")
            #pdf.setFillColorRGB(0,0.35,0.35)
                #Verde pdf.setFillColorRGB(0, 0.44, 0)
            pdf.drawString(500, 770, serie.instalacion.nombre)

            pdf.setFillColor(HexColor('#9ED0B3'))
                #Posición en X, Porición en Y, Largo, alto,
            pdf.rect(0.3 * inch, 10.2 * inch, 7.6 * inch, 0.3 * inch, fill=1)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Helvetica", 11)
            pdf.drawString(170,740, u"Número de pedidos relacionados de clientes CISA")
            pdf.setFillColor(HexColor('#FFFFFF'))
            pdf.rect(0.3 * inch, 9.8 * inch, 7.6 * inch, 0.4 * inch, fill=1)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Helvetica", 8)

            #print((len(serie.no_id_pedido.descripcion)))
            #print(self.obtener_tamano((serie.no_id_pedido.descripcion), 0))

            #pdf.drawString(30,723, serie.no_id_pedido.descripcion)
            content2 = ""
            content3 = 0
            banderasuper = 0
            for legend in serie.no_id_pedido.descripcion:
                #content = str(legend).replace('\n', '<br />\n')
                #content2 += str(legend).replace('\n', '<br />\n')
                content3 += 1
                bandera = self.obtener_tamano2(content3, 0)
                if bandera == 0:
                    content2 += str(legend).replace('\n', '-').replace('\r', '-')
                else:
                    if banderasuper == 0:
                        content2 += str(legend).replace('\n', '') + " -"
                        pdf.drawString(30, 723, content2)
                        content3 = 0
                        content2 = ""
                        banderasuper = 1
                    else:
                        pdf.drawString(30, 713, content2)
                        content3 = 0
                        content2 = ""
                        banderasuper = 0
            pdf.drawString(30, 713, content2)

            pdf.setFillColor(HexColor('#FFFFFF'))
            pdf.rect(0.3 * inch, 9.4 * inch, 7.6 * inch, 0.4 * inch, fill=1)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(30, 693, u"Solicitado por: " +serie.no_id_pedido.solicitado)

            #pdf.setFillColor(HexColor('#d7dfeb'))
            pdf.setFillColor(HexColor('#FFFFFF'))
            pdf.rect(0.3 * inch, 8.3 * inch, 3.8 * inch, 1 * inch, fill=1)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Helvetica", 7)
            pdf.drawString(30, 660, u"Proveedor:")
            pdf.drawString(30, 648, u"Contacto:")
            pdf.drawString(30, 636, u"Teléfono:")
            pdf.drawString(30, 624, u"Dirección:")
            pdf.drawString(30, 612, u"Correo:")
            pdf.drawString(30, 600, u"Anexo:")
            pdf.drawString(68, 660, serie.cod_proveedor.nombre_proveedor)
            pdf.drawString(68, 648, serie.cod_proveedor.contacto_proveedor)
            pdf.drawString(68, 636, serie.cod_proveedor.telefono_proveedor)
            pdf.drawString(68, 624, serie.cod_proveedor.direccion_proveedor)
            pdf.drawString(68, 612, serie.cod_proveedor.correo_proveedor)
            pdf.drawString(68, 600, serie.cod_proveedor.anexo)

            pdf.setFillColor(HexColor('#FFFFFF'))
            pdf.rect(4.15 * inch, 8.3 * inch, 3.75 * inch, 1 * inch, fill=1)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(415, 660, u"Enviar a:")
            pdf.drawString(302, 648, u"Cliente:")
            pdf.drawString(302, 636, u"Contacto:")
            pdf.drawString(302, 624, u"Teléfono:")
            pdf.drawString(302, 612, u"Dirección:")
            pdf.drawString(302, 600, u"Correo:")
            pdf.drawString(337, 648, serie.cod_cliente.nombre_cliente)
            pdf.drawString(337, 636, serie.cod_cliente.contacto_cliente)
            pdf.drawString(337, 624, serie.cod_cliente.telefono_cliente)
            pdf.drawString(337, 612, serie.cod_cliente.direccion_cliente)
            pdf.drawString(337, 600, serie.cod_cliente.correo_cliente)

                # HAce Una LInea
            # pdf.setStrokeColorRGB(0,1,0.3)
            # pdf.line(2,2,2*inch,2*inch)
                #Hace un rectangulo
            #pdf.setFillColorRGB(1, 1, 0)  # choose fill colour
            #pdf.rect(4 * inch, 4 * inch, 2 * inch, 3 * inch, fill=1)  # draw rectangle

    def get(self, request, cod_orden, valor):
        filename = "Orden de Compra_"+cod_orden+".pdf"
            # Indicamos el tipo de contenido a devolver, pdf
        response = HttpResponse(content_type='application/pdf')
            #Descomentar para que solo se descargue
        #response['Content-Disposition'] = 'attachment; filename="%s"' % filename
            # La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
            # Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer, pagesize=A4)
        pdf.setTitle(filename)
        #pdf = Canvas('Reporte.pdf')

        doc = SimpleDocTemplate(
            response,
            pagesize=letter,
            rightMargin=2,
            leftMargin=2,
            topMargin=1,
            bottomMargin=8,
        )
        estructura = []
            # Llamo al metodo cabecera donde estan definidos los datos que aparecen en la cabecera del reporte.
        (self.cabecera(pdf, cod_orden, valor))
        (self.tabla(pdf,250,cod_orden,valor)) #200 para carta
        #doc.build(estructura
            # Con show page hacemos un corte de pagina para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        #response.write(doc.build(estructura))
        response.write(pdf)

        #estiloHoja = getSampleStyleSheet()
        #estilo2 = estiloHoja['Normal']
        #parrafo2 = Paragraph('España, Murcia, Lorca', estilo2)
        #estructura.append(Spacer(100,100))
        #estructura.append(parrafo2)
        #doc.build(estructura)

        return response

    def tabla(self, pdf, y, cod_orden, valor):
        story = []
        #styles = getSampleStyleSheet()

        #hojaEstilo = getSampleStyleSheet()
        #estilo = hojaEstilo['BodyText']
        #P = Paragraph('Un pequeño ejemplo', estilo)
        PAGE_WIDTH = A4[0]
        PAGE_HEIGHT = A4[1]
        #w, h = P.wrap(PAGE_WIDTH, PAGE_HEIGHT)
        #print (w, h)
        #UbicacionParrafo = PAGE_HEIGHT - h
        #P.drawOn(pdf, 0, UbicacionParrafo)

        styles = ParagraphStyle('test')
        styles.textColor = 'black'
        styles.borderColor = 'black'
        styles.alignment = TA_CENTER
        styles.fontSize = 6.5
        # Creamos una tupla de encabezados para neustra tabla
        encabezados = ['CANTIDAD', 'CÓDIGO', 'COLOR', 'FUNCIÓN', 'MEDIDAS\n(ancho x alto)m', 'DESCRIPCIÓN\nDEL PRODUCTO',
                       'PRECIO POR\nUNIDAD (Q)', 'TOTAL (Q)']

            # Creamos una lista de tuplas que van a contener a los producto
        lista_p = []
        #detalles = [(producto.cantidad, producto.codigo, producto.color, producto.funcion, producto.medida, producto.descripcion,
        #             producto.precio, producto.total) for producto in Producto.objects.filter(cod_orden=cod_orden)]
        for producto in Producto.objects.filter(cod_orden=cod_orden):
            po = Paragraph(str(producto.cantidad), styles)
            p1 = Paragraph(str(producto.codigo), styles)
            p2 = Paragraph(str(producto.color), styles)
            p3 = Paragraph(str(producto.funcion), styles)
            p4 = Paragraph(str(producto.medida), styles)
            p5 = Paragraph(str(producto.descripcion), styles)
            p6 = Paragraph(str(producto.precio), styles)
            p7 = Paragraph(str(producto.total), styles)
            lista_p.append((po, p1, p2, p3, p4, p5, p6, p7))

            # Establecemos el tamano de cada una de las columnas de la tabla
        #detalle_orden = Table([encabezados] + detalles, colWidths=[1.2 * cm, 2.5 * cm, 2.3 * cm, 3.2 * cm, 4.2 * cm])
        detalle_orden = Table([encabezados] + lista_p, colWidths=[45, 80, 60, 80, 60, 107, 55, 60])
            # Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#d7dfeb")),
                # La primera fila(encabezados) va a estar centrada
            ('ALIGN', (0, 0), (7, 0), 'CENTER'),
                # Los bordes de todas las celdas serqn de color negro y con un grosor de 1
            ('GRID', (0, 0), (-1, -1), 1, colors.dodgerblue),
                # El tamano de las letras de cada una de las celdas sera de 10
            ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ]))


        w, h = detalle_orden.wrap(PAGE_WIDTH, PAGE_HEIGHT)
        print (w, h)
        UbicacionParrafo = PAGE_HEIGHT - h
        print (UbicacionParrafo)
        #detalle_orden.drawOn(pdf, 0, UbicacionParrafo)

            # Establecemos el tamano de la hoja que ocupara la tabla
        #detalle_orden.wrapOn(pdf, 800, 600)
            # Definimos la coordenada donde se dibujara la tabla
        ubicacion_actual = UbicacionParrafo - y
        print (ubicacion_actual)
        serie = Orden.objects.get(id_orden=cod_orden)
            #Para el salto de pagina
        if ubicacion_actual <= 61:
            print("Producir SAlto de Pagina")
            detalle_orden.drawOn(pdf, 22, ubicacion_actual)
            #pdf.showPage()                                 Para un futuro por si da problemas lo enorme de la tabla
        else:
            detalle_orden.drawOn(pdf, 22, ubicacion_actual)

        pdf.setFont("Helvetica", 8)
        pdf.drawString(145, ubicacion_actual-10, u"|| Total de Metros Cuadrados: "+ str(serie.total_metro))

        producto = Producto.objects.filter(cod_orden=cod_orden)
        total = 0
        for key in producto:
            try:
                total = total + key.total
            except:
                print (".")
        precio= producto.aggregate( precio = Sum(F('total') * F('total')))['precio']
        # print (type(total))
        try:
            precio = total / serie.total_metro
        except:
            precio = 0.00
            print ("..")

        pdf.drawString(287, ubicacion_actual - 10, u"|| Precio por Metro Cuadrado: Q" + "{0:.2f}".format(precio))
        pdf.drawString(480, ubicacion_actual - 10, u"TOTAL: Q")
        pdf.drawString(520, ubicacion_actual - 10, str(total))

        try:
            fecha_entrega = str(serie.fecha_entrega.strftime("%d/%m/%Y"))
        except:
            fecha_entrega = ""

        pdf.drawString(22, ubicacion_actual - 10, u"Fecha de Entrega: " + str(fecha_entrega))

        pdf.drawString(22, ubicacion_actual - 20, u"Tipo de Vidrio: " + str(serie.tipo_vidrio))
        pdf.drawString(145, 25, u"Elaborado por: Gabriela Blanco" )
        pdf.drawString(345, 25, u"Autorizado por: Byron Catalan" )
        pdf.line(125, 35, 275, 35)
        pdf.line(325, 35, 475, 35)


        #story.append(detalle_orden)     #Esto es para que lo agregue en orden, y se pone pdf.buil(story)

    def obtener_tamano(self, valor, cod):
        if cod == 0:
            if int(len(valor)) > 20:
                    # ("Producir Salto")
                return 1
            else:
                    #("Esta dentro del Rango")
                return 0

    def obtener_tamano2(self, valor, cod):
        if cod == 0:
            if int((valor)) > 160:
                    # ("Producir Salto")
                return 1
            if int((valor)) > 120:
                    # ("Producir Salto")
                return 2
            else:
                    #("Esta dentro del Rango")
                return 0