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
    
    def primera_fase(self):
        if not self.valido_para_primera_fase:
            self.participantes_segunda_fase = self.participantes
            self.primera_fase_finalizada = True
            return
        sorteo_aleatorio_primera_fase(self.participantes)        
        self.participantes_segunda_fase = self.participantes.exclude(ganador_primera_fase=True)
        print(self.participantes_segunda_fase)
        self.primera_fase_finalizada = True

    def segunda_fase(self):
        # TO DO: Segunda fase del sorteo: 
        pass


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







def sorteo_aleatorio_primera_fase(queryset):
    if queryset.count() <= 33:
        raise ValueError("Debe haber más de 33 participantes en la primera fase del sorteo.")
    participantes_ganadores_seleccionados = random.sample(list(queryset), 33)
    with transaction.atomic():
        for participante_ganador_seleccionado in participantes_ganadores_seleccionados:
            participante_ganador_seleccionado.ganador = True
            participante_ganador_seleccionado.ganador_primera_fase = True
            participante_ganador_seleccionado.save()
