from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CSVParticipantes, Participante, Sorteo
from .utils import procesar_csv_participantes, crear_sorteo

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
    context['total_participantes'] = Participante.objects.all().count()
    context['participantes'] = Participante.objects.all()
    context['sorteo'] = crear_sorteo()
    return render(request, 'millares.html', context)

def notas(request):
    context = {}
    return render(request, 'notas.html', context)

def herramientas(request):
    context = {}
    return render(request, 'herramientas.html', context)

def reiniciar_sistema(request):
    CSVParticipantes.objects.all().delete()
    Participante.objects.all().delete()
    messages.success(request, 'Sistema reiniciado con éxito.')
    return redirect('main_app:index')

def resetear_ganadores(request):
    Participante.objects.update(
        ganador=None,
        ganador_primera_fase=None,
        ganador_segunda_fase=None
    )
    return redirect('main_app:index')

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

def realizar_sorteo(request):
    # TO DO: Está en proceso de implementación, WIP WIP WIP
    sorteo = crear_sorteo()
    for millar in sorteo.millares:
        millar.primera_fase()
    return redirect('main_app:index')