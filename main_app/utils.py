import csv
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .models import CSVParticipantes, Participante, Sorteo

def procesar_csv_participantes(csv_participantes):
    with open(csv_participantes.csv_file.path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Participante.objects.create(
                millar=row['Millar'],
                posicion_millar=row['Orden'],
                numero_socio=row['Nº Socio'],
                nombre_y_apellidos=row['Nombre']
            )



def crear_sorteo(reorganizar_millares=False):
    participantes = Participante.objects.all()
    sorteo = Sorteo(participantes, reorganizar_millares)
    return sorteo

def realizar_sorteo(sorteo):
    # TO DO: Implementar la lógica del sorteo
    pass