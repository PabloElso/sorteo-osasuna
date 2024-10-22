from django.db import models

# Create your models here.

class CSVParticipantes(models.Model):

    csv_file = models.FileField(upload_to='csvs/')



class Participante(models.Model):

    millar = models.IntegerField()
    posicion_millar = models.IntegerField()
    numero_socio = models.IntegerField()
    nombre_y_apellidos = models.CharField(max_length=100)



class Sorteo:

    def __init__(self, participantes):
        self.participantes = participantes

