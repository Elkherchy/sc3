from rest_framework import serializers
from .models import (
    Calendrier, DisponibilitesEnseignant, PlanningHebdomadaire, 
    ChargeHebdomadaire, ExceptionsPlanning
)

class CalendrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendrier
        fields = '__all__'

class DisponibilitesEnseignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisponibilitesEnseignant
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
