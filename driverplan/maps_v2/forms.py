from django import forms
from .models import Viagem
class RouteForm(forms.Form):
    start = forms.CharField(label='Ponto de Partida', widget=forms.TextInput(attrs={'class': 'form-control'}))
    end = forms.CharField(label='Destino', widget=forms.TextInput(attrs={'class': 'form-control'}))

class ViagemForm(forms.ModelForm):
    class Meta:
        model = Viagem
        fields = ['pontos_de_parada', 'destino', 'origem', 'data_hora', 'motorista', 'cliente']
