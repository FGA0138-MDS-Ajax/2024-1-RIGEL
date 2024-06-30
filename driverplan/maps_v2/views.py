from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .forms import RouteForm
from .models import Rota
from .forms import ViagemForm
from django.shortcuts import render, redirect
from django.contrib import messages  
def index(request):
    form = RouteForm()
    context = {
        'form': form,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'maps/index.html', context)

def save_route_data(request):
    if request.method == 'POST':
        duration = request.POST.get('duration')
        distance = request.POST.get('distance')
        cost = request.POST.get('cost')

        # Salvar os dados no banco de dados
        rota = Rota(duracao=duration, distancia=distance, custo=cost)
        rota.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Método de requisição não suportado'}, status=405)


from django.shortcuts import render, redirect
from django.contrib import messages  # Importar messages
from .forms import ViagemForm

def criar_viagem(request):
    if request.method == 'POST':
        form = ViagemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Viagem salva com sucesso!')
            return redirect('index')  # Redireciona de volta para o index
    else:
        form = ViagemForm()
    return render(request, 'maps/index.html', {'form': form})
