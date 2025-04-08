from django.db import models

class TipoEquipamento(models.Model):
    tipo = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tipo

class FabricanteEquipamento(models.Model):
    fabricante = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.fabricante

class Equipamento(models.Model):
    local = models.ForeignKey('main.local', on_delete=models.CASCADE, related_name='equipamentos')
    tipo = models.ForeignKey('equipamentos.tipoequipamento', on_delete=models.CASCADE, related_name='equipamentos')
    nome_equipamento = models.CharField(max_length=100, unique=True)
    descricao = models.CharField(max_length=100, blank=True, null=True)
    mac = models.CharField(max_length=17, blank=True, null=True, unique=True)  # Formato "00:00:00:00:00:00"
    fabricante = models.ForeignKey('equipamentos.fabricanteequipamento', on_delete=models.CASCADE, related_name='equipamentos')
    patrimonio = models.CharField(max_length=50, unique=True)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo.tipo} - {self.nome_equipamento} ({self.patrimonio})"