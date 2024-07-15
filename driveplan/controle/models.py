from django.db import models
from django.contrib.auth.models import User
from datetime import date

SEXO_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outros')
]

STATUS_CHOICES = [
    ('P', 'PAGO'),
    ('A', 'NÃO PAGO'),
    
]


VALOR_TYPE_CHOICES = [
    ('I', 'Tarifa indireta'),
    ('D', 'Tarifa direta')
]

class Usuario(models.Model):
    cpf = models.CharField(max_length=11, help_text="Número de CPF")
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    whatsapp = models.CharField(max_length=15, help_text="Informe o número no formato (XX) XXXXX-XXXX")
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        abstract = True

    def calcular_idade(self):
        hoje = date.today()
        idade = hoje.year - self.data_nascimento.year
        return idade
    
class Motorista(Usuario):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nome = models.CharField(max_length=255, help_text="Nome Completo")
    nr_cnh = models.CharField(max_length=20, help_text="Número da CNH")
    cep_motorista = models.CharField(max_length=8, help_text="CEP do motorista")
    

    def __str__(self):
        return f"Motorista {self.user.pk}: {self.user.first_name} {self.user.last_name}"

class Documento(models.Model):
    id_documento = models.BigAutoField(primary_key=True)
    motorista_fk = models.ForeignKey(Motorista, on_delete=models.CASCADE)
    nome_documento = models.CharField(max_length=127)
    data_emissao = models.DateField()
    data_vencimento = models.DateField()
    pdf_documento = models.FileField(upload_to='media/data/documentos_file')  # Caminho ajustado
    observacao = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

class Cliente(Usuario):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    id_cliente = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, help_text="Nome Completo")

    def __str__(self):
        return f"{self.nome}"

class Taxa(models.Model):
    id_taxa = models.AutoField(primary_key=True)
    tipo_valor = models.CharField(max_length=1, choices=VALOR_TYPE_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=3)
    descr = models.CharField(max_length=255, help_text="Descrição da taxa")

class Modelo_Viagem_Unico(models.Model):
    id = models.AutoField(primary_key=True)
    motorista_fk = models.ForeignKey(Motorista, on_delete=models.CASCADE)
    taxas_mv_unico = models.ManyToManyField(Taxa)
    #docs_mv_unico = models.ManyToManyField(Documento, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"MODELO:{self.motorista_fk.nome}"

class Viagem_Unica(models.Model):
    id_viagem_unica = models.AutoField(primary_key=True)
    modelo_viagem_unico_fk = models.ForeignKey(Modelo_Viagem_Unico, on_delete=models.CASCADE)
    cliente_fk = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
   
    data_embarque = models.DateField()
    hora_embarque = models.TimeField()
    cep_embarque = models.CharField(max_length=256, help_text="embarque")
    cep_desembarque = models.CharField(max_length=256, help_text="Desembarque")
    data_desembarque_estimado = models.DateField()
    hora_desembarque_estimado = models.TimeField()
    valor_viagem = models.DecimalField(max_digits=10, decimal_places=3)
    observacao = models.CharField(max_length=255, help_text="Observação de Viagem")

    class Meta:
        verbose_name = "Viagem Única"
        verbose_name_plural = "Viagens Únicas"
        unique_together = ('data_embarque', 'hora_embarque')

class Ponto_de_parada(models.Model):
    id_ponto_parada = models.AutoField(primary_key=True)
    viagem_fk = models.ForeignKey(Viagem_Unica, on_delete=models.CASCADE)
    tempo_espera = models.DurationField()
    cep_ponto_parada = models.CharField(max_length=8, help_text="CEP do ponto de parada")
























