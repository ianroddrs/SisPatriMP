from django.shortcuts import render

def movimentacoes(request):
    return render(request, 'movimentacao.html')

