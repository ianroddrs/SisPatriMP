from django.db import models

class Polo(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    polo = models.ForeignKey(Polo, on_delete=models.CASCADE, related_name='cidades')

    def __str__(self):
        return f"{self.nome} ({self.polo.nome})"


class Local(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE, related_name='locais')

    def __str__(self):
        return f"{self.nome} - {self.cidade.nome}"


class TipoEquipamento(models.Model):
    descricao = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.descricao


class Equipamento(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name='equipamentos')
    tipo = models.ForeignKey(TipoEquipamento, on_delete=models.CASCADE, related_name='equipamentos')
    nome = models.CharField(max_length=100)
    dominio = models.CharField(max_length=100, blank=True, null=True)
    mac = models.CharField(max_length=17, blank=True, null=True)  # Formato "00:00:00:00:00:00"
    fabricante = models.CharField(max_length=100)
    patrimonio = models.CharField(max_length=50, unique=True)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo.descricao} - {self.nome} ({self.patrimonio})"


class HistoricoMovimentacao(models.Model):
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, related_name='historico_movimentacao')
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    local_origem = models.ForeignKey(
        Local, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='movimentacoes_origem'
    )
    local_destino = models.ForeignKey(
        Local, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='movimentacoes_destino'
    )
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Movimentação de {self.equipamento.nome} em {self.data_movimentacao:%d/%m/%Y}"
