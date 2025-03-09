from django.db import models
from users.models import User  # Import the User model

# -----------------------
# 📚 Subjects (Matiere)
# -----------------------
class Matiere(models.Model):
    FILIERE_CHOICES = [
        ('TC', 'Tronc Commun'),
        ('DWM', 'Développement Web et Mobile'),
        ('DSI', 'Data Science et Intelligence'),
        ('RSS', 'Réseaux et Systèmes de Sécurité'),
    ]

    matiere_id = models.AutoField(primary_key=True)
    code_matiere = models.CharField(max_length=50)
    nom_matiere = models.CharField(max_length=255)
    credits = models.IntegerField()
    semestre = models.IntegerField()

    filiere = models.CharField(max_length=13, choices=FILIERE_CHOICES)

    def __str__(self):
        return f"{self.nom_matiere} ({self.code_matiere})"


# -----------------------
# 🏫 Groups (Groupes)
# -----------------------
class Groupe(models.Model):
    groupe_id = models.AutoField(primary_key=True)
    semestre = models.IntegerField()
    nom_groupe = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_groupe
from django.db import models

class CalendrierException(models.Model):
    TYPE_EXCEPTION = [
        ("ajout", "Ajout"),  # Adding a new day or time slot
        ("suppression", "Suppression")  # Removing a default time slot
    ]

    JOURS_SEMAINE = [
        ("Lundi", "Lundi"),
        ("Mardi", "Mardi"),
        ("Mercredi", "Mercredi"),
        ("Jeudi", "Jeudi"),
        ("Vendredi", "Vendredi"),
        ("Samedi", "Samedi"),
        ("Dimanche", "Dimanche")  # Only for exceptional cases
    ]

    CRENEAUX_HORAIRES = [
        (1, "08h00 - 09h30"),
        (2, "09h45 - 11h15"),
        (3, "11h30 - 13h00"),
        (4, "15h00 - 16h30"),
        (5, "17h00 - 18h30")
    ]

    jour_semaine = models.CharField(max_length=20, choices=JOURS_SEMAINE)
    creneau_horaire = models.IntegerField(choices=CRENEAUX_HORAIRES)
    type_exception = models.CharField(max_length=20, choices=TYPE_EXCEPTION)
    date = models.DateField()  # The week where the exception applies

    def __str__(self):
        return f"{self.type_exception} - {self.jour_semaine} ({self.get_creneau_horaire_display()}) on {self.date}"


class ChargeHebdomadaire(models.Model):
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    heures_cm = models.IntegerField()
    heures_td = models.IntegerField()
    heures_tp = models.IntegerField()



# -----------------------
# 📚 Group-Subject Relationship (GroupeMatiere)
# -----------------------
class GroupeMatiere(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('groupe', 'matiere')


# -----------------------
# 🧑‍🏫 Teacher-Subject Relationship (MatiereTeacher)
# -----------------------
class MatiereTeacher(models.Model):
    enseignant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'enseignant'})
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('enseignant', 'matiere')


# -----------------------
# 🧑‍🏫 Teacher-Groupe Relationship
# -----------------------
class TeacherGroupe(models.Model):
    enseignant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'enseignant'})
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('enseignant', 'groupe')


# -----------------------
# 📆 Teacher Availability (Disponibilites_Enseignants)
# -----------------------
class DisponibiliteEnseignant(models.Model):
    JOURS_CHOICES = [
        ('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi'),
    ]

    enseignant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'enseignant'})
    jour_semaine = models.CharField(max_length=13, choices=JOURS_CHOICES)
    creneau_horaire = models.IntegerField()

    class Meta:
        unique_together = ('enseignant', 'jour_semaine', 'creneau_horaire')


# -----------------------
# 📅 Weekly Schedule (Planning_Hebdomadaire)
# -----------------------
class PlanningHebdomadaire(models.Model):
    TYPE_LECON_CHOICES = [('CM', 'Cours Magistral'), ('TD', 'Travaux Dirigés'), ('TP', 'Travaux Pratiques')]

    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'enseignant'})
    jour_semaine = models.CharField(max_length=13, choices=DisponibiliteEnseignant.JOURS_CHOICES)
    creneau_horaire = models.IntegerField()
    type_lecon = models.CharField(max_length=2, choices=TYPE_LECON_CHOICES)

    class Meta:
        unique_together = ('groupe', 'matiere', 'enseignant', 'jour_semaine', 'creneau_horaire')


# -----------------------
# 📊 Weekly Workload (Charge_Hebdomadaire)
# -----------------------
class ChargeHebdomadaire(models.Model):
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    heures_cm = models.IntegerField()
    heures_td = models.IntegerField()
    heures_tp = models.IntegerField()

    class Meta:
        unique_together = ('matiere', 'groupe')


# -----------------------
# 🚀 Planning Exceptions (Exceptions_Planning)
# -----------------------
class ExceptionsPlanning(models.Model):
    TYPE_EXCEPTION_CHOICES = [('ajout', 'Ajout'), ('suppression', 'Suppression')]

    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    type_exception = models.CharField(max_length=13, choices=TYPE_EXCEPTION_CHOICES)
    jour_semaine = models.CharField(max_length=13, choices=DisponibiliteEnseignant.JOURS_CHOICES)
    creneau_horaire = models.IntegerField()
    date = models.DateField()

    class Meta:
        unique_together = ('groupe', 'matiere', 'date')
