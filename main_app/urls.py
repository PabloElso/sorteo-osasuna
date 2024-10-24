from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('procesar_participantes_csv/', views.procesar_participantes_csv, name='procesar_participantes_csv'),
    path('participantes/', views.participantes, name='participantes'),
    path('millares/', views.millares, name='millares'),
    path('notas/', views.notas, name='notas'),
    # Add other app-specific URLs here
]