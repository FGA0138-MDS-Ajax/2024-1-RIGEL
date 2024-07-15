# Generated by Django 5.0.6 on 2024-07-09 15:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cliente",
            fields=[
                ("cpf", models.CharField(help_text="Número de CPF", max_length=11)),
                ("data_nascimento", models.DateField()),
                (
                    "sexo",
                    models.CharField(
                        choices=[
                            ("M", "Masculino"),
                            ("F", "Feminino"),
                            ("O", "Outros"),
                        ],
                        max_length=1,
                    ),
                ),
                (
                    "whatsapp",
                    models.CharField(
                        help_text="Informe o número no formato (XX) XXXXX-XXXX",
                        max_length=15,
                    ),
                ),
                ("id_cliente", models.AutoField(primary_key=True, serialize=False)),
                ("nome", models.CharField(help_text="Nome Completo", max_length=255)),
            ],
            options={
                "verbose_name": "Usuário",
                "verbose_name_plural": "Usuários",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Motorista",
            fields=[
                ("cpf", models.CharField(help_text="Número de CPF", max_length=11)),
                ("data_nascimento", models.DateField()),
                (
                    "sexo",
                    models.CharField(
                        choices=[
                            ("M", "Masculino"),
                            ("F", "Feminino"),
                            ("O", "Outros"),
                        ],
                        max_length=1,
                    ),
                ),
                (
                    "whatsapp",
                    models.CharField(
                        help_text="Informe o número no formato (XX) XXXXX-XXXX",
                        max_length=15,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("nr_cnh", models.CharField(help_text="Número da CNH", max_length=20)),
                (
                    "cep_motorista",
                    models.CharField(help_text="CEP do motorista", max_length=8),
                ),
            ],
            options={
                "verbose_name": "Usuário",
                "verbose_name_plural": "Usuários",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Taxa",
            fields=[
                ("id_taxa", models.AutoField(primary_key=True, serialize=False)),
                (
                    "tipo_valor",
                    models.CharField(
                        choices=[("I", "Tarifa indireta"), ("D", "Tarifa direta")],
                        max_length=1,
                    ),
                ),
                ("valor", models.DecimalField(decimal_places=3, max_digits=10)),
                (
                    "descr",
                    models.CharField(help_text="Descrição da taxa", max_length=255),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Documento",
            fields=[
                (
                    "id_documento",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("nome_documento", models.CharField(max_length=127)),
                ("data_emissao", models.DateField()),
                ("data_vencimento", models.DateField()),
                (
                    "pdf_documento",
                    models.FileField(upload_to="media/data/documentos_file"),
                ),
                ("observacao", models.CharField(max_length=255)),
                (
                    "motorista_fk",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="controle.motorista",
                    ),
                ),
            ],
            options={
                "verbose_name": "Documento",
                "verbose_name_plural": "Documentos",
            },
        ),
        migrations.CreateModel(
            name="Modelo_Viagem_Unico",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "docs_mv_unico",
                    models.ManyToManyField(
                        blank=True, null=True, to="controle.documento"
                    ),
                ),
                (
                    "motorista_fk",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="controle.motorista",
                    ),
                ),
                ("taxas_mv_unico", models.ManyToManyField(to="controle.taxa")),
            ],
        ),
        migrations.CreateModel(
            name="Viagem_Unica",
            fields=[
                (
                    "id_viagem_unica",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("P", "PAGO"),
                            ("A", "ATIVO"),
                            ("S", "CANCELADO SEM DEBITO"),
                            ("C", "CANCELADO COM DEBITO"),
                        ],
                        max_length=1,
                    ),
                ),
                ("data_embarque", models.DateField()),
                ("hora_embarque", models.TimeField()),
                (
                    "cep_embarque",
                    models.CharField(help_text="CEP de embarque", max_length=8),
                ),
                (
                    "cep_desembarque",
                    models.CharField(help_text="CEP de desembarque", max_length=8),
                ),
                ("data_desembarque_estimado", models.DateField()),
                ("hora_desembarque_estimado", models.TimeField()),
                ("valor_viagem", models.DecimalField(decimal_places=3, max_digits=10)),
                (
                    "observacao",
                    models.CharField(help_text="Observação de Viagem", max_length=255),
                ),
                ("data_desembarque_efetivo", models.DateField(blank=True, null=True)),
                ("hora_desembarque_efetivo", models.TimeField(blank=True, null=True)),
                (
                    "cliente_fk",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="controle.cliente",
                    ),
                ),
                (
                    "modelo_viagem_unico_fk",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="controle.modelo_viagem_unico",
                    ),
                ),
            ],
            options={
                "verbose_name": "Viagem Única",
                "verbose_name_plural": "Viagens Únicas",
                "unique_together": {("data_embarque", "hora_embarque")},
            },
        ),
        migrations.CreateModel(
            name="Ponto_de_parada",
            fields=[
                (
                    "id_ponto_parada",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("tempo_espera", models.DurationField()),
                (
                    "cep_ponto_parada",
                    models.CharField(help_text="CEP do ponto de parada", max_length=8),
                ),
                (
                    "viagem_fk",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="controle.viagem_unica",
                    ),
                ),
            ],
        ),
    ]