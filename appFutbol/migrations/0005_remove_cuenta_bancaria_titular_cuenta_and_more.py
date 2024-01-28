# Generated by Django 4.2.9 on 2024-01-28 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appFutbol', '0004_alter_cliente_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuenta_bancaria',
            name='titular_cuenta',
        ),
        migrations.RemoveField(
            model_name='datosusuario',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='datosusuario',
            name='partidos_jugados',
        ),
        migrations.RemoveField(
            model_name='dueñorecinto',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='jugador_partido',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='jugador_partido',
            name='partido',
        ),
        migrations.RemoveField(
            model_name='partido',
            name='campo_reservado',
        ),
        migrations.RemoveField(
            model_name='partido',
            name='creador',
        ),
        migrations.RemoveField(
            model_name='partido',
            name='usuarios_jugadores',
        ),
        migrations.RemoveField(
            model_name='post',
            name='creador_post',
        ),
        migrations.RemoveField(
            model_name='promocion',
            name='miusuario',
        ),
        migrations.RemoveField(
            model_name='recinto',
            name='dueño_recinto',
        ),
        migrations.RemoveField(
            model_name='resultado',
            name='resultado_partido',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='votacion_partido',
            name='creador_votacion',
        ),
        migrations.RemoveField(
            model_name='votacion_partido',
            name='partido_votado',
        ),
        migrations.DeleteModel(
            name='Cliente',
        ),
        migrations.DeleteModel(
            name='Cuenta_bancaria',
        ),
        migrations.DeleteModel(
            name='DatosUsuario',
        ),
        migrations.DeleteModel(
            name='Dueñorecinto',
        ),
        migrations.DeleteModel(
            name='Jugador_partido',
        ),
        migrations.DeleteModel(
            name='Partido',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='Promocion',
        ),
        migrations.DeleteModel(
            name='Recinto',
        ),
        migrations.DeleteModel(
            name='Resultado',
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
        migrations.DeleteModel(
            name='Votacion_partido',
        ),
    ]
