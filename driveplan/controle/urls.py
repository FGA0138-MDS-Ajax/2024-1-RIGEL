# controle/urls.py
from django.urls import path
from . import views


app_name = 'controle'


urlpatterns = [
    path('', views.home_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/',views.register_view, name='register'),
    path('home/', views.home_nova, name='home'),
    path('cliente/', views.register_cliente_view, name='cliente'),
    path('formulario/', views.register_viagem_unica_view, name='formulario'),
    path('home/events', views.viagem_unica_events, name='events'),
    path("home_base/", views.home2,name='home_base'),
    path('home/cronograma/', views.home_cronograma, name='home_cronograma'),
    path("home/caledario/", views.home_caledario,name='home_caledario'),
    path('cronograma/', views.cronograma, name='cronograma'),
    path('aceitar_evento/', views.aceitar_evento, name='aceitar_evento'),
    path('recusar_evento/', views.recusar_evento, name='recusar_evento'),
    path('home/unico/',views.criar_viagem_com_taxas, name='unico'),
    path('excluir_viagem/<int:viagem_id>/', views.excluir_viagem, name='excluir_viagem'),
    path('home/finaceiro/', views.ganhos_motoristas, name='home_finaceiro'),
    path('recusar_evento/', views.recusar_evento, name='recusar_evento'),
    path('alterar_status_pagamento/<int:viagem_id>/', views.alterar_status_pagamento, name='alterar_status_pagamento'),
    path('excluir_evento/', views.excluir_evento, name='excluir_evento'),
]
