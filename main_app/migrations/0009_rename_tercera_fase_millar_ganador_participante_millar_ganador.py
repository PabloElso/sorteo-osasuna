# Generated by Django 5.0.1 on 2024-11-04 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_participante_tercera_fase_millar_ganador_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participante',
            old_name='tercera_fase_millar_ganador',
            new_name='millar_ganador',
        ),
    ]
