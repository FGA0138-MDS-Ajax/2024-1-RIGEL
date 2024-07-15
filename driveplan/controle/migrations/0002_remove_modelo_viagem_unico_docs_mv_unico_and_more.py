# Generated by Django 5.0.6 on 2024-07-14 03:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("controle", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="modelo_viagem_unico",
            name="docs_mv_unico",
        ),
        migrations.AddField(
            model_name="motorista",
            name="nome",
            field=models.CharField(
                default="none", help_text="Nome Completo", max_length=255
            ),
            preserve_default=False,
        ),
    ]
