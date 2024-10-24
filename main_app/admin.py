from django.contrib import admin
from .models import CSVParticipantes, Participante

@admin.register(CSVParticipantes)
class CSVParticipantesAdmin(admin.ModelAdmin):
    list_display = ('id', 'csv_file')
    search_fields = ('csv_file',)

    def uploaded_at(self, obj):
        return obj.csv_file.field.upload_to

@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'millar', 'posicion_millar', 'numero_socio', 'nombre_y_apellidos')
    search_fields = ('numero_socio', 'nombre_y_apellidos')
    list_filter = ('millar', 'posicion_millar')

    def get_ordering(self, request):
        return ['millar', 'posicion_millar']

    def get_list_display_links(self, request, list_display):
        return ['nombre_y_apellidos']