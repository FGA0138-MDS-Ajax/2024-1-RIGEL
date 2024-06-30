from django.urls import path
from . import views

app_name = 'maps_v2'  # Namespace para evitar conflitos de URL

urlpatterns = [
    path('', views.index, name='index'),
    path('save_route_data/', views.save_route_data, name='save_route_data'),
    path('criar_viagem/', views.criar_viagem, name='criar_viagem'),  # URL para criar viagem
]
