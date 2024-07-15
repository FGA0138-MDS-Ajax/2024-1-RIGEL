from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from .models import Motorista
from django.contrib.auth.decorators import login_required
from .models import Viagem_Unica
from django.views.decorators.http import require_POST

from datetime import datetime, timedelta
from django.http import JsonResponse

from django.db.models import Sum


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('controle:home')  # Redirecione para a página inicial ou qualquer outra página
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('controle:login')


def home_view(request):
    return render(request, 'index.html')




@login_required(login_url='controle:login')
def home_nova(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Salvando o usuário
            user = form.save()
            
            # Criando o motorista associado ao usuário
            Motorista.objects.create(
                user=user,
                nome=form.cleaned_data.get('nome'),
                cpf=form.cleaned_data.get('cpf'),
                data_nascimento=form.cleaned_data.get('data_nascimento'),
                sexo=form.cleaned_data.get('sexo'),
                whatsapp=form.cleaned_data.get('whatsapp'),
                nr_cnh=form.cleaned_data.get('nr_cnh'),
                cep_motorista=form.cleaned_data.get('cep_motorista')
            )

            # Autenticando e logando o usuário automaticamente após o registro
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            return redirect('controle:home')  # Redireciona para 'home' após o registro

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


from .forms import ClienteForm
from .models import Cliente

def register_cliente_view(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data.get('cpf')

            # Verifica se o CPF já existe
            if Cliente.objects.filter(cpf=cpf).exists():
                form.add_error('cpf', 'Um cliente com este CPF já está registrado.')
            else:
                # Obtém os dados do formulário
                data_nascimento = form.cleaned_data.get('data_nascimento')
                sexo = form.cleaned_data.get('sexo')
                whatsapp = form.cleaned_data.get('whatsapp')
                nome = form.cleaned_data.get('nome')

                # Cria o cliente
                Cliente.objects.create(
                    cpf=cpf,
                    data_nascimento=data_nascimento,
                    sexo=sexo,
                    whatsapp=whatsapp,
                    nome=nome
                )
                return redirect('controle:formulario')  # Redireciona para a lista de clientes após o registro
    else:
        form = ClienteForm()

    return render(request, 'cliente.html', {'form': form})


# views.py

from .forms import ViagemUnicaForm
from .models import Viagem_Unica
from django.urls import reverse

def register_viagem_unica_view(request):
    if request.method == 'POST':
        form = ViagemUnicaForm(request.POST)
        if form.is_valid():
            # Preenchendo o valor_viagem a partir do formulário
            form.instance.valor_viagem = form.cleaned_data['valor_viagem']
            form.save()
            return redirect(reverse('controle:formulario'))  # Redirecionar após salvar
    else:
        form = ViagemUnicaForm()
    return render(request, 'formulario.html', {'form': form})


def viagem_unica_events(request):
    viagens = Viagem_Unica.objects.all()
    events = []

    for viagem in viagens:
        events.append({
            'id': viagem.id_viagem_unica,
            'title': viagem.cliente_fk.nome,  # Usar apenas o nome do cliente como título
            'start': f"{viagem.data_embarque}T{viagem.hora_embarque}",
            'end': f"{viagem.data_desembarque_estimado}T{viagem.hora_desembarque_estimado}",
            'description': viagem.observacao,
            'color': 'green' if viagem.status_cor == 'V' else 'red',  # Definir como verde se o status for 'A'
        })

    return JsonResponse(events, safe=False)

@login_required(login_url='controle:login')
def viagem_unica_events(request):
    try:
        motorista = request.user.motorista
    except Motorista.DoesNotExist:
        motorista = None

    if motorista:
        events = Viagem_Unica.objects.filter(modelo_viagem_unico_fk__motorista_fk=motorista)
        event_list = []
        for event in events:
            event_list.append({
                'title': f"{event.cliente_fk.nome}",
                'start': f"{event.data_embarque}T{event.hora_embarque}",
                'end': f"{event.data_desembarque_estimado}T{event.hora_desembarque_estimado}",
                'cliente': event.cliente_fk.nome,
                'data_embarque': event.data_embarque.strftime('%Y-%m-%d'),
                'hora_embarque': event.hora_embarque.strftime('%H:%M:%S'),
                'cep_embarque': event.cep_embarque,
                'data_desembarque_estimado': event.data_desembarque_estimado.strftime('%Y-%m-%d'),
                'hora_desembarque_estimado': event.hora_desembarque_estimado.strftime('%H:%M:%S'),
                'cep_desembarque': event.cep_desembarque,
                'valor_viagem': f"{event.valor_viagem:.2f}",
                'observacao': event.observacao,
                'status': event.get_status_display(),
            })
        return JsonResponse(event_list, safe=False)
    else:
        return JsonResponse({'error': 'Usuário não é um motorista'}, status=403)

def cronograma(request):
    try:
        motorista = request.user.motorista
    except Motorista.DoesNotExist:
        motorista = None

    if motorista:
        # Lógica para buscar as viagens do motorista
        filtro = request.GET.get('filtro')
        hoje = datetime.now().date()

        if filtro == 'dia':
            viagens = Viagem_Unica.objects.filter(modelo_viagem_unico_fk__motorista_fk=motorista, data_embarque=hoje)
        elif filtro == 'semana':
            data_inicial_semana = hoje - timedelta(days=hoje.weekday())
            data_final_semana = data_inicial_semana + timedelta(days=6)
            viagens = Viagem_Unica.objects.filter(modelo_viagem_unico_fk__motorista_fk=motorista, data_embarque__range=[data_inicial_semana, data_final_semana])
        elif filtro == 'mes':
            primeiro_dia_mes = hoje.replace(day=1)
            ultimo_dia_mes = primeiro_dia_mes.replace(month=primeiro_dia_mes.month + 1, day=1) - timedelta(days=1)
            viagens = Viagem_Unica.objects.filter(modelo_viagem_unico_fk__motorista_fk=motorista, data_embarque__range=[primeiro_dia_mes, ultimo_dia_mes])
        else:
            viagens = Viagem_Unica.objects.filter(modelo_viagem_unico_fk__motorista_fk=motorista)

        data = [{
            'cliente': viagem.cliente_fk.nome,
            'data_embarque': viagem.data_embarque.strftime('%Y-%m-%d'),
            'hora_embarque': viagem.hora_embarque.strftime('%H:%M:%S'),
            'cep_embarque': viagem.cep_embarque,
            'data_desembarque_estimado': viagem.data_desembarque_estimado.strftime('%Y-%m-%d'),
            'hora_desembarque_estimado': viagem.hora_desembarque_estimado.strftime('%H:%M:%S'),
            'cep_desembarque': viagem.cep_desembarque,
            'valor_viagem': f"{viagem.valor_viagem:.2f}",
            'observacao': viagem.observacao,
           
            'status': viagem.get_status_display(),
        } for viagem in viagens]

        return JsonResponse(data, safe=False)
    else:
        # Tratamento caso o usuário não seja um motorista
        return JsonResponse({'error': 'Usuário não é um motorista'}, status=403)



def home2(request):
    return render(request, 'home_base.html')

def home_caledario(request):
    return render(request, 'home_caledario.html')

def home_cronograma(request):
    return render(request, 'home_cronograma.html')

from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from .models import Viagem_Unica

    
from .forms import TaxaForm
from .models import Modelo_Viagem_Unico

@login_required(login_url='controle:login')
def criar_viagem_com_taxas(request):
    modelos_viagem = Modelo_Viagem_Unico.objects.filter(motorista_fk__user=request.user)
    
    if request.method == 'POST':
        taxa_form = TaxaForm(request.POST)
        
        if taxa_form.is_valid():
            taxa = taxa_form.save()
            
            motorista = request.user.motorista  # Acesse o objeto Motorista diretamente
            modelo_viagem = Modelo_Viagem_Unico.objects.create(motorista_fk=motorista)
            modelo_viagem.taxas_mv_unico.add(taxa)  # Adiciona a taxa ao modelo de viagem
            
            # Atualiza a lista de modelos de viagem após a criação
            modelos_viagem = Modelo_Viagem_Unico.objects.filter(motorista_fk__user=request.user)
            
            return redirect('controle:unico')  # Redireciona para uma página de sucesso ou outra view
        
    else:
        taxa_form = TaxaForm()
    
    return render(request, 'home_unico.html', {'taxa_form': taxa_form, 'modelos_viagem': modelos_viagem})
from django.shortcuts import get_object_or_404, redirect
from .models import Modelo_Viagem_Unico

@login_required(login_url='controle:login')
def excluir_viagem(request, viagem_id):
    modelo_viagem = get_object_or_404(Modelo_Viagem_Unico, pk=viagem_id)
    
    # Verifica se o usuário logado é o proprietário do modelo de viagem
    if modelo_viagem.motorista_fk.user != request.user:
        # Se não for o proprietário, retorna um erro ou redireciona para uma página de erro
        # Aqui você pode decidir o comportamento desejado para usuários que não têm permissão
        # Para este exemplo, vamos redirecionar para a página inicial
        return redirect('controle:unico')
    
    # Se for o proprietário, exclui o modelo de viagem
    modelo_viagem.delete()
    
    # Redireciona para uma página de sucesso ou outra view
    return redirect('controle:unico')
@login_required(login_url='controle:login')

def ganhos_motoristas(request):
    # Calcular total pago e obter viagens pagas com detalhes do cliente
    viagens_pagas = Viagem_Unica.objects.filter(status='P').select_related('cliente_fk')
    total_pago = viagens_pagas.aggregate(Sum('valor_viagem'))['valor_viagem__sum'] or 0

    # Viagens com status diferente de "pago" e detalhes do cliente
    viagens_nao_pagas = Viagem_Unica.objects.exclude(status='P').select_related('cliente_fk')

    context = {
        'total_pago': total_pago,
        'viagens_pagas': viagens_pagas,
        'viagens_nao_pagas': viagens_nao_pagas,
    }
    return render(request, 'home_finaceiro.html', context)

from django.views.decorators.csrf import csrf_exempt

import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def recusar_evento(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        viagem = get_object_or_404(Viagem_Unica, id_viagem_unica=event_id)
        
        # Remover o evento do calendário
        viagem.delete()  # Remove o evento do banco de dados

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Método inválido'}, status=405)

    
def aceitar_evento(request):
    if request.method == 'POST' and 'event_id' in request.POST:
        event_id = request.POST['event_id']
        try:
            evento = Viagem_Unica.objects.get(id_viagem_unica=event_id)
            evento.status_cor = 'V'  # Definir status_cor como 'V' (VERDE)
            evento.save()
            return JsonResponse({'success': True})
        except Viagem_Unica.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Evento não encontrado.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'ID do evento não fornecido ou método inválido.'})
    
    
def alterar_status_pagamento(request, viagem_id):
    try:
        viagem = Viagem_Unica.objects.get(id_viagem_unica=viagem_id)
        viagem.status = 'P'  # Altera o status para "Pago"
        viagem.save()

        return redirect('controle:home_finaceiro')
    except Viagem_Unica.DoesNotExist:
        return render(request, '404.html')  # Página de erro 404 ou outra ação desejada
    
from .models import Viagem_Unica



@csrf_exempt
def excluir_evento(request):
    if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
        event_id = request.POST.get('id_viagem_unica')
        try:
            event = Viagem_Unica.objects.get(id_viagem_unica=event_id)
            event.delete()
            return JsonResponse({'message': 'Viagem excluída com sucesso.'}, status=200)
        except Viagem_Unica.DoesNotExist:
            return JsonResponse({'error': 'Viagem não encontrada.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido. Utilize o método POST com "_method=DELETE".'}, status=405)