from django.contrib import admin

from estoque_v2.models import CategoriaFerramenta, Ferramenta, ReservaFerramenta

# Register your models here.
admin.site.register(CategoriaFerramenta)
admin.site.register(Ferramenta)
admin.site.register(ReservaFerramenta)