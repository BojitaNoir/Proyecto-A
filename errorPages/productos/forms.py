#Vamos a crear formularios para cada modulo de la app/modulo
from .models import Producto
from django import forms

#Crear una clase por cada formulario que necesitemos
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'imagen']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre del producto'
                }
            ),
            'precio': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el precio del producto'
                }
            ),
            'imagen': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la URL de la imagen del producto'
                }
            )
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'precio': 'Precio (MXN)',
            'imagen': 'URL de la imagen'
        }
        error_messages = {
            'precio':{
                'required': 'El precio no puede estar vacio',
                'invalid': 'Ingresa un valor valido'
            }
        }
        