from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .models import CSVParticipantes

def comprobar_hay_un_csv():
    count = CSVParticipantes.objects.count()
    if count == 1:
        csv_participante = CSVParticipantes.objects.first()
        if csv_participante.csv_file:
            return True
    return False