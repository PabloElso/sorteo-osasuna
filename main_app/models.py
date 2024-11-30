import random
import csv
import secrets
import os
from django.conf import settings
from django.db import models
from django.db.models import Q

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
    millar_ganador = models.IntegerField(null=True, blank=True)

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

    def __init__(self, codigo):
        self.codigo = codigo
    
    def __str__(self):
        return f'Millar {self.codigo}'
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def participantes(self):
        return Participante.objects.filter(millar=self.codigo)

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
    def participantes_ganadores_en_este_millar(self):
        return Participante.objects.filter(millar_ganador=self.codigo)
    
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
    def participantes_no_ganadores(self):
        return Participante.objects.filter(millar=self.codigo).exclude(ganador=True)
    
    @property
    def cuenta_participantes_no_ganadores(self):
        return self.participantes_no_ganadores.count()

    def primera_fase(self):
        print(f'Fase 1 del millar {self.codigo}')
        if not self.valido_para_primera_fase:
            self.participantes.update(ganador_primera_fase=False)
            return
        ganadores = sorteo_aleatorio(self.participantes, 33)
        ganadores.update(ganador=True, ganador_primera_fase=True, millar_ganador=self.codigo)
        self.participantes.exclude(ganador=True).update(reserva_tercera_fase=True, ganador_primera_fase=False)

    def segunda_fase(self):
        print(f'Fase 2 del millar {self.codigo}')
        if not self.valido_para_segunda_fase:
            self.participantes.update(ganador_segunda_fase=False)
            return
        self.participantes.update(ganador=True, ganador_segunda_fase=True, millar_ganador=self.codigo)
        self.participantes.exclude(ganador=True).update(ganador_segunda_fase=False)
    
    def tercera_fase(self):
        print(f'Fase 3 del millar {self.codigo}')
        if not self.valido_para_tercera_fase:
            self.participantes.exclude(ganador_tercera_fase=True).update(ganador_tercera_fase=False)
            return
        self.participantes.update(ganador=True, ganador_tercera_fase=True, millar_ganador=self.codigo)
        participantes_de_reserva = Participante.objects.filter(reserva_tercera_fase=True).order_by('numero_socio')
        numero_participantes_reserva = participantes_de_reserva.count()
        puestos_vacantes = 33 - self.cuenta_participantes
        # print(f'Puestos vacantes: {puestos_vacantes} - Número de participantes en reserva: {numero_participantes_reserva}')
        if participantes_de_reserva.exists():
            ganadores = sorteo_aleatorio(participantes_de_reserva, puestos_vacantes)
            ganadores.update(ganador=True, reserva_tercera_fase=False, ganador_tercera_fase=True, millar_ganador=self.codigo)


### Definición de función de sorteo aleatorio

def sorteo_aleatorio(queryset, numero_ganadores):
    pks = list(queryset.values_list('pk', flat=True))
    print(f'Cuantos ganadores tiene que haber: {numero_ganadores} - Cuantos participan: {len(pks)}')
    if numero_ganadores > len(pks):
        numero_ganadores = len(pks)
        print(f'ARREGLO: Ahora el número de ganadores es: {numero_ganadores}')
    # selected_pks = random.sample(pks, numero_ganadores)
    print('Generando sorteo aleatorio con la librería secrets')
    selected_pks = secrets.SystemRandom().sample(pks, numero_ganadores)
    return queryset.filter(pk__in=selected_pks)        
        

class Millar_Tras_Sorteo(Millar):

    @property
    def participantes(self):
        complex_filter = (Q(millar=self.codigo) & (Q(millar_ganador=self.codigo) | Q(millar_ganador=None))) | Q(millar_ganador=self.codigo)
        return Participante.objects.filter(complex_filter)


class Sorteo:

    def __init__(self, participantes, reorganizar_millares=False):
        self.participantes = participantes
        self.generar_millares(reorganizar_millares)

    def generar_millares(self, reorganizar_millares):
        if reorganizar_millares:
            MillarClass = Millar_Tras_Sorteo
        else:
            MillarClass = Millar
        millares = []
        listado_codigos_millar = Participante.objects.all().order_by('millar').values_list('millar', flat=True).distinct()
        for codigo_millar in listado_codigos_millar:
            millar = MillarClass(codigo_millar)
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
                'ganador_tercera_fase', 'reserva_tercera_fase', 'fase_ganada', 'millar_ganador',
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
                    participante.fase_ganada,
                    participante.millar_ganador,
                ])
    
    def guardar_resultado_pdf(self):
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer, PageBreak
        from reportlab.lib.units import inch
        import os
        from django.conf import settings
        from datetime import datetime

        subfolder_path = os.path.join(settings.MEDIA_ROOT, 'resultado_sorteo')
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        file_path = os.path.join(subfolder_path, 'resultado_sorteo.pdf')
        doc = SimpleDocTemplate(file_path, pagesize=letter,
                                rightMargin=inch, leftMargin=inch,
                                topMargin=inch, bottomMargin=inch)
        elements = []
        styles = getSampleStyleSheet()

        logo_path = os.path.join(settings.STATIC_ROOT, 'escudo.png')
        if os.path.exists(logo_path):
            logo = Image(logo_path)
            logo.drawHeight = 1 * inch
            logo.drawWidth = 1 * inch
            elements.append(logo)
            elements.append(Spacer(1, 0.2 * inch))

        title_style = ParagraphStyle(name='TitleStyle', parent=styles['Title'], fontSize=24, spaceAfter=10, alignment=1, underline=True)
        title = Paragraph("Elecciones Asamblea", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2 * inch))

        for millar in self.millares:
            millar_title_style = ParagraphStyle(name='MillarTitleStyle', parent=styles['Heading2'], fontSize=18, alignment=1)
            millar_title = Paragraph(f"Millar {millar.codigo}", millar_title_style)
            elements.append(millar_title)
            elements.append(Spacer(1, 0.1 * inch))

            winners_table_title = Paragraph("Participantes seleccionados", styles['Heading3'])
            elements.append(winners_table_title)
            elements.append(Spacer(1, 0.1 * inch))

            winners_data = [['Número Socio', 'Nombre y Apellidos']]
            for participante in millar.participantes_ganadores_en_este_millar:
                winners_data.append([participante.numero_socio, participante.nombre_y_apellidos])
            winners_table = Table(winners_data)
            winners_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(winners_table)
            elements.append(Spacer(1, 0.1 * inch))

            reserves_table_title = Paragraph("Reservas", styles['Heading3'])
            elements.append(reserves_table_title)
            elements.append(Spacer(1, 0.1 * inch))

            reserves_data = [['#', 'Número Socio', 'Nombre y Apellidos']]
            for idx, participante in enumerate(millar.participantes_no_ganadores.filter(reserva_tercera_fase=True), start=1):
                reserves_data.append([idx, participante.numero_socio, participante.nombre_y_apellidos])
            reserves_table = Table(reserves_data)
            reserves_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(reserves_table)
            elements.append(Spacer(1, 0.2 * inch))

            elements.append(Spacer(1, 0.5 * inch))
            elements.append(PageBreak())

        def add_footer(canvas, doc):
            footer_text = datetime.now().strftime('%d/%m/%Y %H:%M')
            footer = Paragraph(footer_text, styles['Normal'])
            width, height = letter
            footer.wrapOn(canvas, width, height)
            footer.drawOn(canvas, inch, 0.5 * inch)

            page_number_text = f"Página {doc.page}"
            page_number = Paragraph(page_number_text, styles['Normal'])
            page_number.wrapOn(canvas, width, height)
            page_number.drawOn(canvas, width - inch, 0.5 * inch)

        doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)