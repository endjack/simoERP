from django.db import models

# Create your models here.

class Cliente(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    doc = models.CharField(max_length=50, null=True, blank=True)
    cargo = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return "{} - {}".format(self.nome, self.cargo)
    

  
