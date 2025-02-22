from django.http import HttpResponse
from django.shortcuts import render
from .utils import google_search

def index(request):
    return HttpResponse("<h1>Hola Mundo<h1>")

def error_404_view(request):
    render(request, '404.html', status=404)

def error_500_view(request):
    render(request, '500.html', status=500)

def error(request, exception):
    return 7/0

def onepage(request):
    return render(request, 'onepage.html', status=200)

def search_view(request):
    query = request.GET.get("q", "")
    results = []
    if query:
        data = google_search(query)
        results = data.get("items", [])

    return render(request, "search.html", {"results": results, "query": query})


def prueba(request):
    #Como obtener informacion de un HTML
    nombre = request.GET.get('nombre','')
    edad = request.GET.get('edad','')

    persona = {
        'nombres':nombre,
        'edad':edad,
        'descripcion': nombre + ' - ' + edad 
    }

    persona2 = {
        'nombres': 'Jaime',
        'edad': '30',
        'descripcion': nombre + ' - ' + edad 
    }

    persona3 = {
        'nombres': 'Ayala',
        'edad': '16',
        'descripcion': nombre + ' - ' + edad 
    }



    if(persona['nombres'] == 'Adrian'):
        persona['descripcion'] = 'Bienvenido usuario administrador'
    
    print(persona['nombres'])
    conjunto = [persona,persona2,persona3]

    return render(
        request, 
        'prueba.html', 
        {'objeto':persona , 'saludo':'Hola Mundo', 'personas':conjunto}
    )


from django.http import JsonResponse
from django.shortcuts import render
from .models import ErrorLog

def error_logs(request):
    return render(request, 'error_logs.html')

def get_error_logs(request):
    errors = ErrorLog.objects.values('id', 'codigo', 'mensaje', 'fecha')
    return JsonResponse({'data': list(errors)})

