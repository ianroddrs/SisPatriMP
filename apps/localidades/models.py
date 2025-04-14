from django.db import models

class Polo(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    polo = models.ForeignKey('localidades.polo', on_delete=models.CASCADE, related_name='cidades')

    def __str__(self):
        return f"{self.nome} ({self.polo.nome})"


class Local(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.ForeignKey('localidades.cidade', on_delete=models.CASCADE, related_name='locais')

    def __str__(self):
        return f"{self.nome} - {self.cidade.nome}"


class HistoricoMovimentacao(models.Model):
    equipamento = models.ForeignKey('equipamentos.equipamento', on_delete=models.CASCADE, related_name='historico_movimentacao')
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    local_origem = models.ForeignKey(
        'localidades.local', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='movimentacoes_origem'
    )
    local_destino = models.ForeignKey(
        'localidades.local', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='movimentacoes_destino'
    )
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Movimentação de {self.equipamento.nome} em {self.data_movimentacao:%d/%m/%Y}"