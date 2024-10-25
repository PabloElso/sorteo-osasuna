import random
from django.db import models, transaction

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
    ganador_primera_fase = models.BooleanField(null=True, blank=True)
    ganador_segunda_fase = models.BooleanField(null=True, blank=True)
    ganador_tercera_fase = models.BooleanField(null=True, blank=True)
    reserva_tercera_fase = models.BooleanField(default=False, blank=True)

    class Meta:
        verbose_name = 'Participante'
        verbose_name_plural = 'Participantes'
        ordering = ['millar', 'posicion_millar', 'numero_socio', 'nombre_y_apellidos']


class Millar:

    def __init__(self, codigo, participantes):
        self.codigo = codigo
        self.participantes = participantes
        self.primera_fase_finalizada = False
        self_segunda_fase_finalizada = False
        self.finalizado = False
    
    def __str__(self):
        return f'Millar {self.codigo}'
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def cuenta_participantes(self):
        return self.participantes.count()
    
    @property
    def valido_para_primera_fase(self):
        return self.cuenta_participantes > 33
    
    @property
    def valido_para_segunda_fase(self):
        return self.cuenta_participantes == 33
    
    @property
    def valido_para_tercera_fase(self):
        return self.cuenta_participantes < 33
    
    def primera_fase(self):
        if not self.valido_para_primera_fase:
            return
        sorteo_aleatorio(self.participantes, 33)
        self.participantes.filter(ganador=True).update(ganador_primera_fase=True)
        self.participantes.exclude(ganador=True).update(reserva_tercera_fase=True)

    def segunda_fase(self):
        if not self.valido_para_segunda_fase:
            return
        self.participantes.update(ganador=True, ganador_segunda_fase=True)
    
    def tercera_fase(self):
        if not self.valido_para_tercera_fase:
            return
        self.participantes.update(ganador=True, ganador_tercera_fase=True)
        participantes_de_reserva = Participante.objects.filter(reserva_tercera_fase=True).order_by('numero_socio')
        numero_participantes_reserva = participantes_de_reserva.count()
        puestos_vacantes = 33 - self.cuenta_participantes
        print(f'Puestos vacantes: {puestos_vacantes} - Número de participantes en reserva: {numero_participantes_reserva}')
        if participantes_de_reserva.exists():
            sorteo_aleatorio(participantes_de_reserva, puestos_vacantes)
            # Se eliminan los ganadores de la reserva
            participantes_de_reserva.filter(reserva_tercera_fase=True, ganador=True).update(reserva_tercera_fase=False, ganador_tercera_fase=True)

        
        


class Sorteo:

    def __init__(self, participantes):
        self.participantes = participantes
        self.generar_millares()

    def generar_millares(self):
        millares = []
        listado_codigos_millar = Participante.objects.all().order_by('millar').values_list('millar', flat=True).distinct()
        for codigo_millar in listado_codigos_millar:
            participantes = Participante.objects.filter(millar=codigo_millar)
            millar = Millar(codigo_millar, participantes)
            millares.append(millar)
        self.millares = millares







def sorteo_aleatorio(queryset, numero_ganadores):
    participantes_ganadores_seleccionados = random.sample(list(queryset), numero_ganadores)
    with transaction.atomic():
        for participante_ganador_seleccionado in participantes_ganadores_seleccionados:
            participante_ganador_seleccionado.ganador = True
            participante_ganador_seleccionado.save()
        
