from django.db import models

# Create your models here.

class CSVParticipantes(models.Model):

    csv_file = models.FileField(upload_to='csvs/')

    class Meta:
        verbose_name = 'CSV de participantes'
        verbose_name_plural = 'CSVs de participantes'


class Participante(models.Model):

    millar = models.IntegerField()
    posicion_millar = models.IntegerField()
    numero_socio = models.IntegerField()
    nombre_y_apellidos = models.CharField(max_length=100)
    ganador = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name = 'Participante'
        verbose_name_plural = 'Participantes'
        ordering = ['millar', 'posicion_millar', 'numero_socio', 'nombre_y_apellidos']


class Millar:

    def __init__(self, numero, participantes):
        self.numero = numero
        self.participantes = participantes


class Sorteo:

    def __init__(self, participantes):
        self.participantes = participantes

