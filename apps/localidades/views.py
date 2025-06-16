from django.shortcuts import render
from core.models import Regioes
# from 

def localidades(request):
    action = request.POST.get('action', None)
    
    regioes = Regioes.objects.prefetch_related('cidades').all()
    
    cidades_regiao = {}

    for regiao in regioes:
        cidades = [cidade.nome for cidade in regiao.cidades.all()]
        cidades_regiao[regiao.nome] = cidades
    
    context = {
        'cidades_regiao': cidades_regiao
    }
    
    if action == 'adicionar_local':
        # cidade, _ = Cidade.objects.get_or_create(nome=request.GET.get('cidade'))
        # local, _ = Local.objects.get_or_create(nome=request.GET.get('local'), cidade=cidade)
        pass
    return render(request, 'localidades.html', context)

