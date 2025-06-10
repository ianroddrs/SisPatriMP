from django.shortcuts import render
# from 

def localidades(request):
    action = request.POST.get('action', None)
    
    if action == 'adicionar_local':
        # cidade, _ = Cidade.objects.get_or_create(nome=request.GET.get('cidade'))
        # local, _ = Local.objects.get_or_create(nome=request.GET.get('local'), cidade=cidade)
        pass
    return render(request, 'localidades.html')

