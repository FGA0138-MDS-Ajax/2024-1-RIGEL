from django.shortcuts import render, redirect
from django.conf import settings
from .forms import RouteForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from .forms import RegistroForm

def registrar(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registrar.html', {'form': form})


@login_required
def protected_view(request):
    return render(request, 'protected.html')

@permission_required('app_label.permission_codename')
def view_with_permission(request):
    return render(request, 'permission.html')

def login_view(request):
    if request.method == 'GET':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def index(request):
    form = RouteForm()
    context = {
        'form': form,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    }

    return render(request, 'index.html', context)
