from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CSVParticipantes, Participante, Sorteo
from .utils import procesar_csv_participantes

# Create your views here.

def index(request):
    context = {}
    context['total_csvs'] = CSVParticipantes.objects.all().count()
    context['total_participantes'] = Participante.objects.all().count()
    context['participantes'] = Participante.objects.all()
    return render(request, 'index.html', context)


def participantes(request):
    context = {}
    context['total_participantes'] = Participante.objects.all().count()
    context['participantes'] = Participante.objects.all()
    return render(request, 'participantes.html', context)

def millares(request):
    context = {}
    return render(request, 'millares.html', context)

def notas(request):
    context = {}
    return render(request, 'notas.html', context)

def procesar_participantes_csv(request):
    if CSVParticipantes.objects.all().count() == 0:
        messages.warning(request, 'No hay ningún CSV de participantes para procesar.')
        return redirect('main_app:index')
    if CSVParticipantes.objects.all().count() > 1:
        messages.warning(request, 'Hay más de un CSV, no se realizará el procesado hasta que solamente haya uno.')
        return redirect('main_app:index')
    if Participante.objects.all().count() > 0:
        messages.warning(request, 'Ya hay participantes en la base de datos. Borra todos los participantes si quieres procesar un nuevo CSV.')
        return redirect('main_app:index')
    csv_participantes = CSVParticipantes.objects.first()
    procesar_csv_participantes(csv_participantes)
    return redirect('main_app:index')