# Generated by Django 3.2.10 on 2025-02-24 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juegos', '0028_rename_puntaje_general_partidajugador_puntaje'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='puntaje_general',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
