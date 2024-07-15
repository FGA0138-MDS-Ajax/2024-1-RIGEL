from django.contrib import admin
from .models import Motorista, Documento, Cliente, Taxa, Modelo_Viagem_Unico, Viagem_Unica, Ponto_de_parada

admin.site.register(Motorista)
admin.site.register(Documento)
admin.site.register(Cliente)
admin.site.register(Taxa)
admin.site.register(Modelo_Viagem_Unico)
admin.site.register(Viagem_Unica)
admin.site.register(Ponto_de_parada)


