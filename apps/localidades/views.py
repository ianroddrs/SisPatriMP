from django.shortcuts import render

def localidades(request):
    return render(request, 'localidades.html')

