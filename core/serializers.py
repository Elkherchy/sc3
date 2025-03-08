from rest_framework import serializers
from .models import Enseignant, Groupe, Matiere, MatiereEnseignant, MatiereGroupe, TeacherGroupe

# Serializer for Enseignant
class EnseignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enseignant
        fields = ['id', 'nom', 'identifiant']

# Serializer for Matiere
class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = ['id', 'code_matiere', 'nom_matiere', 'credits', 'semestre', 'filiere']

# Serializer for Groupe
class GroupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupe
        fields = ['id', 'semestre', 'nom_groupe']

# Serializer for MatiereEnseignant (Teacher-Matiere relationship)
class MatiereEnseignantSerializer(serializers.ModelSerializer):
    enseignant = EnseignantSerializer()
    matiere = MatiereSerializer()

    class Meta:
        model = MatiereEnseignant
        fields = ['id', 'enseignant', 'matiere']

# Serializer for MatiereGroupe (Matiere-Groupe relationship)
class MatiereGroupeSerializer(serializers.ModelSerializer):
    groupe = GroupeSerializer()
    matiere = MatiereSerializer()

    class Meta:
        model = MatiereGroupe
        fields = ['id', 'groupe', 'matiere']

# Serializer for TeacherGroupe (Teacher-Groupe relationship)
class TeacherGroupeSerializer(serializers.ModelSerializer):
    enseignant = EnseignantSerializer()
    groupe = GroupeSerializer()

    class Meta:
        model = TeacherGroupe
        fields = ['id', 'enseignant', 'groupe']
