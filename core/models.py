from django.db import models
from django.contrib.auth.models import User # Importar o modelo User do Django

class Regioes(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    regiao = models.ForeignKey('regioes', on_delete=models.CASCADE, related_name='cidades')

    def __str__(self):
        return f"{self.nome} ({self.regiao.nome})"


class Local(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.ForeignKey('cidade', on_delete=models.CASCADE, related_name='locais')
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.cidade.nome}"


class HistoricoMovimentacao(models.Model):
    equipamento = models.ForeignKey('equipamento', on_delete=models.CASCADE, related_name='historico_movimentacao')
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    local_origem = models.ForeignKey(
        'local',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movimentacoes_origem'
    )
    local_destino = models.ForeignKey(
        'local',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movimentacoes_destino'
    )
    observacao = models.TextField(blank=True, null=True)
    # Adicionado o campo 'usuario' para rastrear quem fez a movimentação
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimentacoes_realizadas')

    def __str__(self):
        return f"Movimentação de {self.equipamento.nome_equipamento} em {self.data_movimentacao:%d/%m/%Y}"


class TipoEquipamento(models.Model):
    tipo = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tipo


class FabricanteEquipamento(models.Model):
    fabricante = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.fabricante


class Equipamento(models.Model):
    local = models.ForeignKey('local', on_delete=models.CASCADE, related_name='equipamentos')
    tipo = models.ForeignKey('tipoequipamento', on_delete=models.CASCADE, related_name='equipamentos')
    nome_equipamento = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100, blank=True, null=True)
    mac = models.CharField(max_length=17, blank=True, null=True, unique=True)  # Formato "00:00:00:00:00:00"
    fabricante = models.ForeignKey('fabricanteequipamento', on_delete=models.CASCADE, related_name='equipamentos')
    patrimonio = models.CharField(max_length=50, unique=True)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo.tipo} - {self.nome_equipamento} ({self.patrimonio})"
