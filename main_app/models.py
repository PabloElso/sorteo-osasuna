import random
import csv
import os
from django.conf import settings
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

    @property
    def fase_ganada(self):
        if self.ganador_tercera_fase:
            return 3
        elif self.ganador_segunda_fase:
            return 2
        elif self.ganador_primera_fase:
            return 1
        else:
            return 0

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
    
    @property
    def participantes_ganadores(self):
        return self.participantes.filter(ganador=True)
    
    @property
    def cuenta_participantes_ganadores(self):
        return self.participantes_ganadores.count()
    
    @property
    def participantes_ganadores_primera_fase(self):
        return self.participantes_ganadores.filter(ganador_primera_fase=True)
    
    @property
    def participantes_ganadores_segunda_fase(self):
        return self.participantes_ganadores.filter(ganador_segunda_fase=True)
    
    @property
    def participantes_ganadores_tercera_fase(self):
        return self.participantes_ganadores.filter(ganador_tercera_fase=True)
    
    @property
    def cuenta_participantes_ganadores_primera_fase(self):
        return self.participantes_ganadores_primera_fase.count()
    
    @property
    def cuenta_participantes_ganadores_segunda_fase(self):
        return self.participantes_ganadores_segunda_fase.count()
    
    @property
    def cuenta_participantes_ganadores_tercera_fase(self):
        return self.participantes_ganadores_tercera_fase.count()
    
    @property
    def participantes_reserva(self):
        return self.participantes.filter(reserva_tercera_fase=True).order_by('numero_socio')
    
    @property
    def participantes_no_ganadores(self):
        return self.participantes.exclude(ganador=True)
    
    @property
    def cuenta_participantes_no_ganadores(self):
        return self.participantes_no_ganadores.count()

    def primera_fase(self):
        if not self.valido_para_primera_fase:
            self.participantes.update(ganador_primera_fase=False)
            return
        sorteo_aleatorio(self.participantes, 33)
        self.participantes.filter(ganador=True).update(ganador_primera_fase=True)
        self.participantes.exclude(ganador=True).update(reserva_tercera_fase=True, ganador_primera_fase=False)

    def segunda_fase(self):
        if not self.valido_para_segunda_fase:
            self.participantes.update(ganador_segunda_fase=False)
            return
        self.participantes.update(ganador=True, ganador_segunda_fase=True)
        self.participantes.exclude(ganador=True).update(ganador_segunda_fase=False)
    
    def tercera_fase(self):
        if not self.valido_para_tercera_fase:
            self.participantes.update(ganador_tercera_fase=False)
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
    
    def guardar_resultado_csv(self):
        subfolder_path = os.path.join(settings.MEDIA_ROOT, 'resultado_sorteo')
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        file_path = os.path.join(subfolder_path, 'resultado_sorteo.csv')
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                'millar', 'posicion_millar', 'numero_socio', 'nombre_y_apellidos',
                'ganador', 'ganador_primera_fase', 'ganador_segunda_fase',
                'ganador_tercera_fase', 'reserva_tercera_fase', 'fase_ganada'
            ])
            for participante in self.participantes:
                writer.writerow([
                    participante.millar,
                    participante.posicion_millar,
                    participante.numero_socio,
                    participante.nombre_y_apellidos,
                    participante.ganador,
                    participante.ganador_primera_fase,
                    participante.ganador_segunda_fase,
                    participante.ganador_tercera_fase,
                    participante.reserva_tercera_fase,
                    participante.fase_ganada
                ])
    
    def guardar_resultado_pdf(self):
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
        from reportlab.lib.units import inch
        import os
        from django.conf import settings

        subfolder_path = os.path.join(settings.MEDIA_ROOT, 'resultado_sorteo')
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        file_path = os.path.join(subfolder_path, 'resultado_sorteo.pdf')
        doc = SimpleDocTemplate(file_path, pagesize=letter,
                                rightMargin=inch, leftMargin=inch,
                                topMargin=inch, bottomMargin=inch)
        elements = []
        styles = getSampleStyleSheet()
        title = Paragraph("Resultados del Sorteo", styles['Title'])
        intro_text = Paragraph("A continuación se presentan los resultados del sorteo:", styles['BodyText'])
        elements.append(title)
        elements.append(intro_text)
        data = [['Millar', 'Posición Millar', 'Número Socio', 'Nombre y Apellidos', 'Ganador', 'Fase Ganada']]
        for participante in self.participantes:
            nombre_y_apellidos = Paragraph(participante.nombre_y_apellidos, styles['BodyText'])
            data.append([
                participante.millar,
                participante.posicion_millar,
                participante.numero_socio,
                nombre_y_apellidos,
                "Sí" if participante.ganador else "No",
                participante.fase_ganada
            ])
        col_widths = [0.5*inch, 1*inch, 1*inch, 1.5*inch, 0.75*inch, 1*inch]
        table = Table(data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightblue, colors.lightcoral]),
            ('WORDWRAP', (0, 0), (-1, 0), 'CJK'),
        ]))
        elements.append(table)
        doc.build(elements)



### Definición de función de sorteo aleatorio

def sorteo_aleatorio(queryset, numero_ganadores):
    participantes_ganadores_seleccionados = random.sample(list(queryset), numero_ganadores)
    with transaction.atomic():
        for participante_ganador_seleccionado in participantes_ganadores_seleccionados:
            participante_ganador_seleccionado.ganador = True
            participante_ganador_seleccionado.save()
        
