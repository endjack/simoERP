from financeiro.models import *
from django.contrib import admin

# Register your models here.

admin.site.register(ContaPagamento)
admin.site.register(Pagamento)
admin.site.register(TagConta)
admin.site.register(ItensNota)
admin.site.register(PagamentoTemp)
admin.site.register(DescricaoNota)
admin.site.register(NotaCompleta)
admin.site.register(PagamentoVista)
admin.site.register(ContaBoleto)