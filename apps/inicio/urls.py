from django.conf.urls import url
from apps.inicio.views import *
from apps.inicio import views
from django.contrib.auth.views import logout
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', login, name='login'),
    url(r'^admon/$', my_login_required(UserList.as_view()), name='admon'),
    url(r'^newUser/$', my_login_required(UsuarioCreate.as_view()), name='usuario_crear'),
    url(r'^updateUser/(?P<pk>\d+)/$', my_login_required(UsuarioUpdate.as_view()), name='usuario_actualizar'),
    url(r'^deleteUser/(?P<codigo>\d+)/$', my_login_required(UsuarioDelete), name='usuario_eliminar'),

    url(r'^OrdenList/', my_login_required(OrdenList.as_view()), name='ordenes'),
    url(r'^OrdenDetalle/(?P<pk>\d+)/$', my_login_required(OrdenDetalle), name='detalle_orden'),
    url(r'^nuevaOrden/$', my_login_required(OrdenCreate.as_view()), name='orden_crear'),
    url(r'^mis_ordenes/(?P<valor>\d+)/', my_login_required(MyOrden), name='mi_orden'),
    url(r'^CambiarOrden/(?P<cod_orden>\d+)/(?P<valor>\d+)/$', my_login_required(Cambiar_Orden), name='cambiar_orden'),

    url(r'^busqueda/(?P<id>\d+)/(?P<valor>\d+)/', my_login_required(Busqueda), name='buscar'),

    url(r'^O_P_Detalle/(?P<pk>\d+)/(?P<valor>\d+)/$', my_login_required(OpCreate), name='op_create'),

    url(r'^salir/$', logout, name='salir', kwargs={'next_page': '/'}),
    url(r'^404Not/$', error, name='error'),
    url(r'^error/$', error2, name='error2'),

    # url(r'^reporte_pdf/$',my_login_required(some_view), name="reporte_pdf"),
    url(r'^reporte_pdf/(?P<cod_orden>\d+)/(?P<valor>\d+)/$',my_login_required(ReporteOrdenPDF.as_view()), name="reporte_pdf2"),

    # purebas
    url(r'^prueba1/$', views.prueba_list, name='prueba11'),
    url(r'^prueba1/(?P<pk>[0-9]+)/$', views.prueba_detail, name='prueba12'),
    url(r'^prueba2/$', views.Prueba2List.as_view(), name='prueba21'),
    url(r'^prueba2/(?P<pk>[0-9]+)/$', views.Prueba2Detail.as_view(), name='prueba22'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
