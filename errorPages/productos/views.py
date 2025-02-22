import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Producto
from .forms import ProductoForm

#Metodo que devuelve el JSON
def lista_productos(request):
    productos = Producto.objects.all()

    #Contruir una variable en formato de diccionario porque el JSONResponse lo requiere
    data = [
        {
            #Objeto producto construido al aire
            'nombre': p.nombre,
            'precio': p.precio,
            'imagen': p.imagen
        }
        for p in productos
    ]

    #Devolver la respuesta en JSON
    return JsonResponse(data, safe=False)

#Funcion para mandar a la vista del form
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agregar')
    else:
        form = ProductoForm()
    return render(request, 'agregar.html', {'form': form})

#Funcion que registre sin recrgar la pagina (Sin hacer render)

def registrar_producto(request):
    #Checar que estemos manejando POST
    if request.method == 'POST':
        try:
            #Intentar obtener los datos del body del request
            data = json.loads(request.body)#Hace que el prarametro devuelva un JSON
            producto = Producto.objects.create(
                #Basicamente es un constructor
                nombre = data['nombre'],
                precio = data['precio'],
                imagen = data['imagen']
            ) #La funcion create directamente ingresa el modelo a la BD
            return JsonResponse({'message': 'Registro exitoso','id': producto.id}, status=201)
        except Exception as e:
            return JsonResponse({'error' :str(e)}, status=400)
    return JsonResponse({'error': 'Metodo no soportado'}, status=405)    

#El metodo del API PUT
#PUT = Actualizar
def actualizar_producto(request, id_producto):
    if request.method == 'PUT':
        #Voy a intentar Actualizar
        #1) Pso obtener la entidad / modelo especifico a actualizar
        #Parametros: Modelo y id o identificador
        producto = get_object_or_404(Producto, id=id_producto)
        try:
            #Vamos a actualizar         
            #2) Con la informacion que deberiamos estar recibiendo en el cuerpo rques
            data = json.loads(request.body)
            #3) Actualizar cada campo disponible de la entidad
            producto.nombre = data.get('nombre', producto.nombre)
            producto.precio = data.get('precio', producto.precio)
            producto.imagen = data.get('imagen', producto.imagen)
            producto.save()
            #4) Es retornar una respuesta de que todo salio bien
            return JsonResponse({'message': 'Producto actualizado correctamente'}, status=200)
        except Exception as e:
            #5) Si algo falla, devolver un error
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Metodo no soportado'}, status=405)

#El metodo del API DELETE
def borrar_producto(request, id_producto):
    if request.method == 'DELETE':
        producto = get_object_or_404(Producto, id=id_producto)
        producto.delete() #<-- Esto borra fisicamente en la base de datos
        return JsonResponse({'message': 'Producto eliminado correctamente'}, status=200)
    return JsonResponse({'error': 'Metodo no soportado'}, status=405)

#Metodo que devuelve solo 1 objeto de la BD
def obtener_producto(request, id_producto):
    if request.method == 'GET':
        producto = get_object_or_404(Producto, id=id_producto)
        data = {
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': producto.precio,
            'imagen': producto.imagen
        }
        return JsonResponse(data, status=200)
    return JsonResponse({'error': 'Metodo no soportado'}, status=405)