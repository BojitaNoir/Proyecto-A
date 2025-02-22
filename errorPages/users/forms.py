from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth import authenticate
import re

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Contraseña',
                'required': True,
                'pattern': '^(?=.*\d)(?=.*[A-Z])(?=.*[!#$%&?])[A-Za-z\d!#$%&?]{8,}$',
                'title': 'La contraseña debe contener al menos 8 caracteres, 1 número, 1 letra mayúscula y 1 carácter especial.',
            }
        )
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirmar contraseña',
                'required': True,
                'pattern': '^(?=.*\d)(?=.*[A-Z])(?=.*[!#$%&?])[A-Za-z\d!#$%&?]{8,}$',
                'title': 'La contraseña debe contener al menos 8 caracteres, 1 número, 1 letra mayúscula y 1 carácter especial.',
            }
        )
    )    
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'surname', 'control_number', 'age', 'tel', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico',
                'required': True,
                'pattern': '^[a-zA-Z0-9._%+-]+@utez\.edu\.mx$',
                'title': 'Debes ingresar un correo de la UTEZ',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre',
                'required': True,
                'title': 'Ingresa tu nombre',
            }),
            'surname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido',
                'required': True,
                'title': 'Ingresa tu apellido',
            }),
            'control_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de control',
                'pattern': '^\d{5}TN\d{3}$',
                'required': True,
                'title': 'Ingresa tu número de control',
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Edad',
                'required': True,
                'title': 'Ingresa tu edad',
            }),
            'tel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono',
                'required': True,
                'pattern': '^\d{10}$',
                'title': 'El numero de telefono debe de ser de 10 numeros',
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not re.match(r"^[a-zA-Z0-9._%+-]+@utez\.edu\.mx$", email):
            raise forms.ValidationError("Debes usar un correo de la UTEZ (ejemplo: 20223tn097@utez.edu.mx).")
        return email

    def clean_control_number(self):
        control_number = self.cleaned_data.get("control_number")
        if not re.match(r"^\d{5}TN\d{3}$", control_number):
            raise forms.ValidationError("Formato incorrecto (ejemplo: 20223TN073).")
        return control_number

    def clean_tel(self):
        tel = self.cleaned_data.get("tel")
        if not tel.isdigit() or len(tel) != 10:
            raise forms.ValidationError("El teléfono debe contener exactamente 10 dígitos numéricos.")
        return tel

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age < 0 or age > 120:
            raise forms.ValidationError("La edad debe estar entre 0 y 120 años.")
        return age


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Correo electrónico",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@utez.edu.mx',
            'required': True
        }),
        max_length=254,
        min_length=5
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'required': True
        }),
        min_length=8,
        max_length=128
    )
    name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre',
            'required': True
        }),
        max_length=100,
        min_length=2
    )
    surname = forms.CharField(
        label="Apellido",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido',
            'required': True
        }),
        max_length=100,
        min_length=2
    )
    control_number = forms.CharField(
        label="Número de control",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '20223TN073',
            'required': True
        }),
        max_length=20,
        min_length=10
    )
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not re.match(r"^(?=.*\d)(?=.*[A-Z])(?=.*[!#$%&?]){8,}$", password):
            raise forms.ValidationError("La contraseña debe contener al menos 8 caracteres, 1 número, 1 letra mayúscula y 1 carácter especial.")
        return password
    

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Usuario o contraseña incorrectos.")
        return cleaned_data
