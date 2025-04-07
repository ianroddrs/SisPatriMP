from django.db import models

class TipoEquipamento(models.Model):
    descricao = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.descricao

class Equipamento(models.Model):
    local = models.ForeignKey('main.local', on_delete=models.CASCADE, related_name='equipamentos')
    tipo = models.ForeignKey('equipamentos.tipoequipamento', on_delete=models.CASCADE, related_name='equipamentos')
    nome = models.CharField(max_length=100)
    dominio = models.CharField(max_length=100, blank=True, null=True)
    mac = models.CharField(max_length=17, blank=True, null=True)  # Formato "00:00:00:00:00:00"
    fabricante = models.CharField(max_length=100)
    patrimonio = models.CharField(max_length=50, unique=True)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo.descricao} - {self.nome} ({self.patrimonio})"