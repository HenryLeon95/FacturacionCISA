from django import forms
from apps.inicio.models import*
from django.forms import modelformset_factory


class LoginForm(forms.ModelForm):
    class Meta:
        model = Usuario

        fields = [
            'contrasena',
            'nombre_usuario',
        ]
        labels = {
            'contrasena': 'Contrasena',
            'nombre_usuario': 'Nombre de usuario',
        }
        widgets = {
            'contrasena':forms.PasswordInput(attrs={'class':'form-control'}),
            'nombre_usuario':forms.TextInput(attrs={'class':'form-control'}),
        }


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario

        fields = [
            'nombre_usuario',
            'contrasena',
            'tipo_rol',
        ]
        labels = {
            'nombre_usuario': 'Nombre de usuario',
            'contrasena': 'Password',
            'tipo_rol': 'Tipo de Rol',
        }
        widgets = {
            'nombre_usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'contrasena': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_rol': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super(UsuarioForm, self).clean()
        user_exists = (Usuario.objects.filter(nombre_usuario = cleaned_data.get('nombre_usuario')).count()>0)
        if user_exists:
            self.add_error('nombre_usuario','Nombre de Usuario ya existente')


class UsuarioForm2(forms.ModelForm):
    class Meta:
        model = Usuario

        fields = [
            'nombre_usuario',
            'contrasena',
            'tipo_rol',
        ]
        labels = {
            'nombre_usuario': 'Nombre de usuario',
            'contrasena': 'Password',
            'tipo_rol': 'Tipo de Rol',
        }
        widgets = {
            'nombre_usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'contrasena': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_rol': forms.Select(attrs={'class': 'form-control'}),
        }


class Pr1(forms.ModelForm):
    class Meta:
        model = Usuario

        fields = [
            'nombre_usuario',
        ]
        labels = {
            'nombre_usuario': 'Nombre de usuario',
        }
        widgets = {
            'nombre_usuario':forms.TextInput(attrs={'class':'form-control'}),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nombre_cliente',
            'contacto_cliente',
            'direccion_cliente',
            'telefono_cliente',
            'correo_cliente',
        ]
        labels = {
            'nombre_cliente': 'Cliente',
            'contacto_cliente': 'Contacto',
            'direccion_cliente': 'Direccion',
            'telefono_cliente': 'Telefono',
            'correo_cliente': 'Correo',
        }
        widgets = {
            'nombre_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_cliente': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            'nombre_proveedor',
            'contacto_proveedor',
            'direccion_proveedor',
            'telefono_proveedor',
            'correo_proveedor',
            'anexo',
        ]
        labels = {
            'nombre_proveedor': 'Proveedor',
            'contacto_proveedor': 'Contacto',
            'direccion_proveedor': 'Direccion',
            'telefono_proveedor': 'Telefono',
            'correo_proveedor': 'Correo',
            'anexo': 'Anexo',
        }
        widgets = {
            'nombre_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'anexo': forms.TextInput(attrs={'class': 'form-control'}),
        }


class NoPedidoForm(forms.ModelForm):
    class Meta:
        model = NoPedido
        fields = [
            'descripcion',
            'solicitado',
        ]
        labels = {
            'descripcion': 'Descripcion',
            'solicitado': 'Solicitado',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form_control', 'cols': 62, 'rows': 5}),
            'solicitado': forms.Textarea(attrs={'class': 'form_control','cols': 62, 'rows': 5}),
        }


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = [
            'cantidad',
            'codigo',
            'color',
            'funcion',
            'medida',
            'descripcion',
            'precio',
            'total',
        ]
        labels = {
            'cantidad' :'Cantidad',
            'codigo': 'Codigo',
            'color': 'Color',
            'funcion': 'Funcion',
            'medida': 'Medidas en metros (ancho x alto)',
            'descripcion': 'Descripcion del producto',
            'precio': 'Precio por unidad (Q)',
            'total': 'Total (Q)',
        }
        widgets = {
            'cantidad': forms.TextInput(attrs={'class': 'form-control', 'min': 0, 'type': 'number'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'funcion': forms.TextInput(attrs={'class': 'form-control'}),
            'medida': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form_control', 'cols': 46, 'rows': 5}),
            'precio': forms.TextInput(attrs={'class': 'form-control', 'min': 0, 'type': 'number'}),
            'total': forms.TextInput(attrs={'class': 'form-control', 'min': 0, 'type': 'number'}),
        }


class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = [
            'serie_orden',
            'instalacion',
            'cancelado',
            'observacion',
            'total_metro',
            'tipo_vidrio',
            'fecha_entrega',
            'fecha_entrega_produccion',
            'fecha_entrega_bodega',
            'fecha_entrega_cliente',
        ]
        labels = {
            'serie_orden': 'Eliga la Serie',
            'instalacion': 'Inclueye Instalacion',
            'cancelado': 'Ya cancelado',
            'observacion': 'Observaciones',
            'total_metro': 'Total de Mts2',
            'tipo_vidrio': 'Tipo de Vidrio',
            'fecha_entrega': 'Fecha de Entrega',
            'fecha_entrega_produccion': 'Fecha de Entrega a Produccion',
             'fecha_entrega_bodega': 'Fecha de entrega a Bodega',
             'fecha_entrega_cliente': 'Fecha de entrega al Cliente',
        }
        widgets = {
            'serie_orden': forms.Select(attrs={'class': 'form-control'}),
            #'instalacion': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'instalacion': forms.Select(attrs={'class': 'form-control'}),
            'cancelado': forms.Select(attrs={'class': 'form-control'}),
            'observacion': forms.Textarea(attrs={'class': 'form_control'}),
            'total_metro': forms.TextInput(attrs={'class': 'form-control', 'min': 0, 'type': 'number'}),
            'tipo_vidrio': forms.TextInput(attrs={'class': 'form-control'}),
            #'fecha_entrega': forms.DateInput(attrs={'class': 'form-control'}),
            'fecha_entrega': forms.DateInput(format=('%d-%m-%Y'), attrs={'class':'myDateClass', 'placeholder':'Year-Month-Day'}),
            'fecha_entrega_produccion': forms.DateInput(format=('%d-%m-%Y'), attrs={'class': 'myDateClass', 'placeholder': 'Year-Month-Day'}),
            'fecha_entrega_bodega': forms.DateInput(format=('%d-%m-%Y'), attrs={'class': 'myDateClass', 'placeholder': 'Year-Month-Day'}),
            'fecha_entrega_cliente': forms.DateInput(format=('%d-%m-%Y'), attrs={'class': 'myDateClass', 'placeholder': 'Year-Month-Day'}),
        }


ProductoFormset = modelformset_factory(Producto, fields=('cantidad', 'codigo', 'color', 'funcion', 'medida', 'descripcion',
            'precio', 'total',), extra=1, widgets={
    'cantidad': forms.TextInput(attrs={'class': 'form-control', 'min': 0, 'type': 'number', 'cols':10}),
    'codigo': forms.Textarea(attrs={'class': 'form_control', 'cols': 7, 'rows': 1}),
    'color': forms.TextInput(attrs={'class': 'form-control'}),
    'funcion': forms.Textarea(attrs={'class': 'form_control', 'cols': 7, 'rows': 1}),
    'medida': forms.Textarea(attrs={'class': 'form_control', 'cols': 7, 'rows': 1}),
    'descripcion': forms.Textarea(attrs={'class': 'form_control', 'cols': 15, 'rows': 3}),
    'precio': forms.TextInput(attrs={'class': 'form-control', 'min': 0, 'type': 'number', 'step':'0.01'}),
    'total': forms.TextInput(attrs={'class': 'form-control', 'min': 0, 'type': 'number', 'step': .01}),
})



