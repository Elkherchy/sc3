from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import (
    Calendrier, DisponibilitesEnseignant, PlanningHebdomadaire, 
    ChargeHebdomadaire, ExceptionsPlanning
)
from .Serializers import (
    CalendrierSerializer,
    DisponibilitesEnseignantSerializer,
    PlanningHebdomadaireSerializer,
    ChargeHebdomadaireSerializer,
    ExceptionsPlanningSerializer
)


# CRUD for Calendrier
@api_view(['GET', 'POST'])
def calendrier_list_create(request):
    if request.method == 'GET':
        calendriers = Calendrier.objects.all()
        serializer = CalendrierSerializer(calendriers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CalendrierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def calendrier_detail(request, pk):
    try:
        calendrier = Calendrier.objects.get(pk=pk)
    except Calendrier.DoesNotExist:
        return Response({'error': 'Calendrier not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CalendrierSerializer(calendrier)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CalendrierSerializer(calendrier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        calendrier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CRUD for DisponibilitesEnseignant
@api_view(['GET', 'POST'])
def disponibilites_list_create(request):
    if request.method == 'GET':
        disponibilites = DisponibilitesEnseignant.objects.all()
        serializer = DisponibilitesEnseignantSerializer(disponibilites, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DisponibilitesEnseignantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def disponibilites_detail(request, pk):
    try:
        disponibilite = DisponibilitesEnseignant.objects.get(pk=pk)
    except DisponibilitesEnseignant.DoesNotExist:
        return Response({'error': 'Disponibilité not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DisponibilitesEnseignantSerializer(disponibilite)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DisponibilitesEnseignantSerializer(disponibilite, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        disponibilite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CRUD for PlanningHebdomadaire
@api_view(['GET', 'POST'])
def planning_list_create(request):
    if request.method == 'GET':
        planning = PlanningHebdomadaire.objects.all()
        serializer = PlanningHebdomadaireSerializer(planning, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PlanningHebdomadaireSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def planning_detail(request, pk):
    try:
        planning = PlanningHebdomadaire.objects.get(pk=pk)
    except PlanningHebdomadaire.DoesNotExist:
        return Response({'error': 'Planning not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlanningHebdomadaireSerializer(planning)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PlanningHebdomadaireSerializer(planning, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        planning.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CRUD for ChargeHebdomadaire
@api_view(['GET', 'POST'])
def charge_list_create(request):
    if request.method == 'GET':
        charges = ChargeHebdomadaire.objects.all()
        serializer = ChargeHebdomadaireSerializer(charges, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ChargeHebdomadaireSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CRUD for ExceptionsPlanning
@api_view(['GET', 'POST'])
def exceptions_list_create(request):
    if request.method == 'GET':
        exceptions = ExceptionsPlanning.objects.all()
        serializer = ExceptionsPlanningSerializer(exceptions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ExceptionsPlanningSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
