from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'identifiant']

class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = '__all__'

class GroupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupe
        fields = '__all__'

class GroupeMatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupeMatiere
        fields = '__all__'

class MatiereTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatiereTeacher
        fields = '__all__'
class CalendrierExceptionSerializer(serializers.ModelSerializer):
    creneau_horaire_display = serializers.CharField(source='get_creneau_horaire_display', read_only=True)

    class Meta:
        model = CalendrierException
        fields = '__all__'
# ✅ Serializer for Charge Hebdomadaire (Weekly Workload)
class ChargeHebdomadaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeHebdomadaire
        fields = '__all__'

class TeacherGroupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherGroupe
        fields = '__all__'

class DisponibiliteEnseignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisponibiliteEnseignant
        fields = '__all__'

class PlanningHebdomadaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanningHebdomadaire
        fields = '__all__'

class ChargeHebdomadaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeHebdomadaire
        fields = '__all__'

class ExceptionsPlanningSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExceptionsPlanning
        fields = '__all__'
