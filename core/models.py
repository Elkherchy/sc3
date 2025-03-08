from django.db import models


class Enseignant(models.Model):
    enseignant_id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    identifiant = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nom

class Matiere(models.Model):
    MATIERE_CHOICES = [
        ('TC', 'TC'),
        ('DWM', 'DWM'),
        ('DSI', 'DSI'),
        ('RSS', 'RSS'),
    ]

    matiere_id = models.AutoField(primary_key=True)
    code_matiere = models.CharField(max_length=50)
    nom_matiere = models.CharField(max_length=255)
    credits = models.IntegerField()
    semestre = models.IntegerField()
    filiere = models.CharField(max_length=4, choices=MATIERE_CHOICES)

    def __str__(self):
        return self.nom_matiere

class Groupe(models.Model):
    groupe_id = models.AutoField(primary_key=True)
    semestre = models.IntegerField()
    nom_groupe = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_groupe

class MatiereGroupe(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('groupe', 'matiere')

    def __str__(self):
        return f"{self.groupe.nom_groupe} - {self.matiere.nom_matiere}"

class MatiereEnseignant(models.Model):
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('enseignant', 'matiere')

    def __str__(self):
        return f"{self.enseignant.nom} - {self.matiere.nom_matiere}"

class TeacherGroupe(models.Model):
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('enseignant', 'groupe')

    def __str__(self):
        return f"{self.enseignant.nom} - {self.groupe.nom_groupe}"