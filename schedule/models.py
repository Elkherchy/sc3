from django.db import models
from core.models import Enseignant, Matiere, Groupe


class Calendrier(models.Model):
    jour = models.CharField(max_length=10, choices=[
        ('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi')
    ])
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    
    def __str__(self):
        return f"{self.jour} ({self.heure_debut} - {self.heure_fin})"

class DisponibilitesEnseignant(models.Model):
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    jour_semaine = models.CharField(max_length=9, choices=[('Lundi', 'Lundi'), ('Mardi', 'Mardi'), 
                                                           ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), 
                                                           ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi')])
    créneau_horaire = models.IntegerField()

    class Meta:
        unique_together = ('enseignant', 'jour_semaine', 'créneau_horaire')

    def __str__(self):
        return f"{self.enseignant.nom} - {self.jour_semaine} - {self.créneau_horaire}"

class PlanningHebdomadaire(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    jour_semaine = models.CharField(max_length=9, choices=[('Lundi', 'Lundi'), ('Mardi', 'Mardi'), 
                                                           ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), 
                                                           ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi')])
    créneau_horaire = models.IntegerField()
    type_lecon = models.CharField(max_length=2, choices=[('CM', 'CM'), ('TD', 'TD'), ('TP', 'TP')])

    class Meta:
        unique_together = ('groupe', 'matiere', 'enseignant', 'jour_semaine', 'créneau_horaire')

    def __str__(self):
        return f"{self.groupe.nom_groupe} - {self.matiere.nom_matiere} - {self.enseignant.nom} - {self.jour_semaine}"

class ChargeHebdomadaire(models.Model):
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    heures_cm = models.IntegerField()
    heures_td = models.IntegerField()
    heures_tp = models.IntegerField()

    class Meta:
        unique_together = ('matiere', 'groupe')

    def __str__(self):
        return f"{self.matiere.nom_matiere} - {self.groupe.nom_groupe}"

class ExceptionsPlanning(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    type_exception = models.CharField(max_length=15, choices=[('ajout', 'ajout'), ('suppression', 'suppression')])
    jour_semaine = models.CharField(max_length=9, choices=[('Lundi', 'Lundi'), ('Mardi', 'Mardi'), 
                                                           ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), 
                                                           ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi')])
    créneau_horaire = models.IntegerField()
    date = models.DateField()

    class Meta:
        unique_together = ('groupe', 'matiere', 'date')

    def __str__(self):
        return f"{self.groupe.nom_groupe} - {self.matiere.nom_matiere} - {self.date} - {self.type_exception}"