from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('procesar_participantes_csv/', views.procesar_participantes_csv, name='procesar_participantes_csv'),
    path('participantes/', views.participantes, name='participantes'),
    path('millares/', views.millares, name='millares'),
    path('notas/', views.notas, name='notas'),
    path('herramientas/', views.herramientas, name='herramientas'),
    path('reiniciar_sistema/', views.reiniciar_sistema, name='reiniciar_sistema'),
    path('resetear_ganadores/', views.resetear_ganadores, name='resetear_ganadores'),
    path('realizar_sorteo/', views.realizar_sorteo, name='realizar_sorteo'),
    # Add other app-specific URLs here
]