from .models import Categoria
from django import forms

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'imagen']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre'
                }
            ),
            'imagen': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la URL de la imagen'
                }
            )
        }
        labels = {
            'nombre': 'Nombre de la Categoria',
            'imagen': 'URL de la imagen'
        }
        error_messages = {
            'nombre':{
                'required': 'El nombre no puede estar vacio',
                'invalid': 'Ingresa un valor valido'
            },
            'imagen':{
                'required': 'La URL de la imagen no puede estar vacia',
                'invalid': 'Ingresa un valor valido'
            },
        }