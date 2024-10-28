from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('subir_csv/', views.subir_csv, name='subir_csv'),
    path('procesar_participantes_csv/', views.procesar_participantes_csv, name='procesar_participantes_csv'),
    path('participantes/', views.participantes, name='participantes'),
    path('millares/', views.millares, name='millares'),
    path('ayuda/', views.ayuda, name='ayuda'),
    path('herramientas/', views.herramientas, name='herramientas'),
    path('reiniciar_sistema/', views.reiniciar_sistema, name='reiniciar_sistema'),
    path('resetear_ganadores/', views.resetear_ganadores, name='resetear_ganadores'),
    path('realizar_sorteo/', views.realizar_sorteo, name='realizar_sorteo'),
    path('descargar_csv_sorteo/', views.descargar_csv_sorteo, name='descargar_csv_sorteo'),
]