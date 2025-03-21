# Generated by Django 5.1.6 on 2025-03-09 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_calendrier'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendrierException',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jour_semaine', models.CharField(choices=[('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi'), ('Dimanche', 'Dimanche')], max_length=20)),
                ('creneau_horaire', models.IntegerField(choices=[(1, '08h00 - 09h30'), (2, '09h45 - 11h15'), (3, '11h30 - 13h00'), (4, '15h00 - 16h30'), (5, '17h00 - 18h30')])),
                ('type_exception', models.CharField(choices=[('ajout', 'Ajout'), ('suppression', 'Suppression')], max_length=20)),
                ('date', models.DateField()),
            ],
        ),
        migrations.DeleteModel(
            name='Calendrier',
        ),
    ]
