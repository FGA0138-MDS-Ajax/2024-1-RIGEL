from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Modelo_Viagem_Unico, Taxa


SEXO_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outros')
]

STATUS_CHOICES = [
    ('P', 'PAGO'),
    ('A', 'PENDENTE')
   
]

class RegisterForm(UserCreationForm):
    nome = forms.CharField(max_length=256, help_text="Nome completo")
    cpf = forms.CharField(max_length=11, help_text="Número de CPF")
    data_nascimento = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    sexo = forms.ChoiceField(choices=SEXO_CHOICES)
    whatsapp = forms.CharField(max_length=15, help_text="Informe o número no formato (XX) XXXXX-XXXX")
    nr_cnh = forms.CharField(max_length=20, help_text="Número da CNH")
    cep_motorista = forms.CharField(max_length=8, help_text="CEP do motorista")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'cpf', 'data_nascimento', 'sexo', 'whatsapp', 'nr_cnh', 'cep_motorista']

from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cpf', 'data_nascimento', 'sexo', 'whatsapp', 'nome']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'sexo': forms.Select(choices=SEXO_CHOICES),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if Cliente.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Já existe um cliente cadastrado com este CPF.")
        return cpf
    
from .models import Viagem_Unica

class ViagemUnicaForm(forms.ModelForm):
    class Meta:
        model = Viagem_Unica
        fields = '__all__'
        labels = {
            'modelo_viagem_unico_fk': 'Escolha Seu Modelo Viagem ',
            'cliente_fk': 'Seu nome',
            'status': 'Status',
            'data_embarque': 'Data de Embarque',
            'hora_embarque': 'Hora de Embarque',
            'cep_embarque': 'CEP de Embarque',
            'cep_desembarque': 'CEP de Desembarque',
            'data_desembarque_estimado': 'Data Estimada de Desembarque',
            'hora_desembarque_estimado': 'Hora Estimada de Desembarque',
            'observacao': 'Observação',
        }
        
        widgets = {
            'valor_viagem': forms.HiddenInput(),  # Campo oculto para o valor da viagem
            'data_embarque': forms.DateInput(attrs={'type': 'date'}),  # Widget para data de embarque
            'hora_embarque': forms.TimeInput(attrs={'type': 'time'}),  # Widget para hora de embarque
            'data_desembarque_estimado': forms.DateInput(attrs={'type': 'date'}),  # Widget para data de desembarque estimado
            'hora_desembarque_estimado': forms.TimeInput(attrs={'type': 'time'}),  # Widget para hora de desembarque estimado
        }
        
        
from .models import Taxa
VALOR_TYPE_CHOICES = [
    ('I', 'Tarifa indireta'),
    ('D', 'Tarifa direta')
]

class TaxaForm(forms.ModelForm):
    tipo_valor = forms.ChoiceField(choices=VALOR_TYPE_CHOICES)

    class Meta:
        model = Taxa
        fields = '__all__'