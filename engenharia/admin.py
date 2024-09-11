from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(OrdemServicoObras)
admin.site.register(CategoriaImagem)
admin.site.register(ImagemOS)
admin.site.register(DocumentoOS)
admin.site.register(DiarioDeObraOs)
admin.site.register(DiarioDeObraContrato)
admin.site.register(ServiçosDiarioDeObraContrato)
admin.site.register(FuncionarioOS)