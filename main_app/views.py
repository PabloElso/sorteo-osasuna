import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.conf import settings
from .models import CSVParticipantes, Participante, Sorteo
from .utils import procesar_csv_participantes, crear_sorteo


CSV_SORTEO = os.path.join(settings.MEDIA_ROOT, 'resultado_sorteo', 'resultado_sorteo.csv')

### Views base

def index(request):
    context = {}
    context['total_csvs'] = CSVParticipantes.objects.all().count()
    context['total_participantes'] = Participante.objects.all().count()
    context['participantes'] = Participante.objects.all()
    context['sorteo_finalizado'] = Participante.objects.filter(ganador=True).count() > 0
    context['existe_csv_sorteo'] = os.path.exists(CSV_SORTEO)
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

def subir_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        try:
            csv_file = request.FILES['csv_file']
            csv_creado = CSVParticipantes(csv_file=csv_file)
            csv_creado.save()
            messages.success(request, 'CSV subido con éxito.')
        except:
            messages.error(request, 'Error al subir el CSV.')
    return redirect('main_app:index')


### Views secundarias: para desarrollo y pruebas principalmente

def ayuda(request):
    context = {}
    return render(request, 'ayuda.html', context)

def herramientas(request):
    context = {}
    return render(request, 'herramientas.html', context)

def reiniciar_sistema(request):
    CSVParticipantes.objects.all().delete()
    Participante.objects.all().delete()
    if os.path.exists(CSV_SORTEO):
        os.remove(CSV_SORTEO)
    CSV_INPUT_FOLDER = os.path.join(settings.MEDIA_ROOT, 'csvs')
    if os.path.exists(CSV_INPUT_FOLDER):
        for filename in os.listdir(CSV_INPUT_FOLDER):
            file_path = os.path.join(CSV_INPUT_FOLDER, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    messages.success(request, 'Sistema reiniciado con éxito.')
    return redirect('main_app:index')

def resetear_ganadores(request):
    Participante.objects.update(
        ganador=None,
        ganador_primera_fase=None,
        ganador_segunda_fase=None, 
        ganador_tercera_fase=None,
        reserva_tercera_fase=False,
    )
    if os.path.exists(CSV_SORTEO):
        os.remove(CSV_SORTEO)
    return redirect('main_app:index')


### Views de procesado de CSVs y sorteo

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
    for millar in sorteo.millares:
        millar.segunda_fase()
    for millar in sorteo.millares:
        millar.tercera_fase()
    # Marcar finalmente aquellos que no han ganado como no ganadores.
    Participante.objects.exclude(ganador=True).update(ganador=False)
    # Guardado del resultado del sorteo en CSV
    sorteo.guardar_resultado_csv()
    return redirect('main_app:index')

def descargar_csv_sorteo(request):
    if os.path.exists(CSV_SORTEO):
        with open(CSV_SORTEO, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(CSV_SORTEO)}'
            return response
    else:
        messages.warning(request, 'No hay ningún CSV de sorteo para descargar.')
        return redirect('main_app:index')