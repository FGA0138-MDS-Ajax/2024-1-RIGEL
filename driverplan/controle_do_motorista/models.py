from django.db import models
from django.contrib.auth.models import User
from datetime import date
from validate_docbr import CPF,CNH

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True,primary_key=True)
    cpf = models.CharField(max_length=11, validators=[CPF().validate], help_text="Número de CPF")
    data_nascimento = models.DateField()
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outros')
    ]
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    whatsapp = models.CharField(max_length=15, help_text="Informe o número no formato (XX) XXXXX-XXXX")

    def calcular_idade(self):
        hoje = date.today()
        ano_nascimento = self.data_nascimento.year
        idade = hoje - ano_nascimento
        return idade

class Motorista(Usuario):
    nr_cnh = models.CharField(max_length=20, validators=[CNH().validate], help_text="Número da CNH") 
    cep_motorista = models.CharField(max_length=8, help_text="CEP do motorista")

    def __str__(self):
        return f"Motorista {self.user.pk}: {self.user.first_name} {self.user.last_name}"

class Cliente(Usuario):
    #cep_cliente = models.CharField(max_length=8, help_text="CEP do cliente")

    def __str__(self):
        return f"Cliente {self.user.pk}: {self.user.first_name} {self.user.last_name}"


class Modelo_de_viagem(models.Model):
    motorista_fk = models.ForeignKey(Motorista,on_delete=models.CASCADE,primary_key=True)
    cliente_fk = models.ForeignKey(Cliente, primary_key=True, on_delete=models.CASCADE)
    data = models.DateField(primary_key=True)
    hora = models.TimeField(primary_key=True)
    PERIODO_CHOICE = [
        ('U', 'Única'),
        ('s', 'Semanal'),
        ('Q', 'Quinzenal'),
        ('M', 'Mensal'),
        ('B', 'Bimestral'),
        ('T', 'Trimestral'),
        ('S', 'Semestral'),
        ('A', 'Anual')
    ]
    periodicidade = models.CharField(max_length=1, choices=PERIODO_CHOICE)
    taxa_por_km = models.DecimalField(max_digits=10, decimal_places=4)
    taxa_emergencial = models.DecimalField(max_digits=10, decimal_places=4)
    taxa_desloc_previo = models.DecimalField(max_digits=10, decimal_places=4)
    taxa_espera = models.DecimalField(max_digits=10, decimal_places=4)
    valor_adicional = models.DecimalField(max_digits=10, decimal_places=4)

class Viagem(models.Model):
    data_viagem = models.DateField(primary_key=True)
    hora_viagem = models.TimeField(primary_key=True)
    motorista_fk = models.ForeignKey(Motorista,on_delete=models.CASCADE,primary_key=True)
    cliente_fk = models.ForeignKey(Cliente, primary_key=True, on_delete=models.CASCADE)
    cep_partida = models.CharField(max_length=8, help_text="CEP de partida")
    cep_chegada = models.CharField(max_length=8, help_text="CEP de chegada")
    STATUS_CHOICES = [
        ('p', 'Pago'),
        ('a', 'Ativo'),
        ('i', 'Inativo')
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

class Ponto_de_parada(models.Model):
    ponto_parada_id = models.AutoField(primary_key=True)
    viagem_fk = models.ForeignKey(Viagem, on_delete=models.CASCADE)
    tempo_espera = models.DurationField()
    cep_ponto_parada = models.CharField(max_length=8, help_text="CEP do ponto de parada")



























class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nr_identidade = models.CharField(max_length=20)  # Número de identidade
    CPF_cliente = models.CharField(max_length=20)
    telefone = models.CharField(max_length=15)
    nome = models.CharField(max_length=100)
    idade = models.PositiveIntegerField()
    sexo = models.CharField(max_length=1)  # 'M' para masculino, 'F' para feminino

class ModeloDeViagem(models.Model):
    data_hora = models.DateTimeField()
    origem = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    pontos_parada = models.TextField()
    periodicidade = models.CharField(max_length=20)  # Diário, semanal, mensal etc.
    taxa_km = models.DecimalField(max_digits=6, decimal_places=2)  # Taxa principal por quilômetro
    taxa_aguardo = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # Taxa de espera (opcional)
    taxa_adicional = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # Outras taxas adicionais

class Agendamento(models.Model):
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    viagem = models.ForeignKey(ModeloDeViagem, on_delete=models.CASCADE)
    aceitou_viagem = models.BooleanField(default=False)
    # Outros campos relacionados ao agendamento
