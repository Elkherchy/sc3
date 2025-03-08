# views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Enseignant, Groupe, Matiere, MatiereEnseignant, MatiereGroupe, TeacherGroupe
from .serializers import EnseignantSerializer, GroupeSerializer, MatiereSerializer, MatiereEnseignantSerializer, MatiereGroupeSerializer, TeacherGroupeSerializer

# List Enseignants
@api_view(['GET'])
def enseignant_list(request):
    enseignants = Enseignant.objects.all()
    serializer = EnseignantSerializer(enseignants, many=True)
    return Response(serializer.data)

# Create Enseignant
@api_view(['POST'])
def create_enseignant(request):
    if request.method == 'POST':
        serializer = EnseignantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Enseignant created successfully', 'id': serializer.data['id']}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Update Enseignant (PUT)
@api_view(['PUT', 'DELETE'])
def update_enseignant(request, pk):
    enseignant = get_object_or_404(Enseignant, pk=pk)
    if request.method == 'PUT':
        serializer = EnseignantSerializer(enseignant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Enseignant updated successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        enseignant.delete()
        return Response({'message': 'Enseignant deleted successfully'}, status=status.HTTP_200_OK)

# List Matieres
@api_view(['GET'])
def matiere_list(request):
    matieres = Matiere.objects.all()
    serializer = MatiereSerializer(matieres, many=True)
    return Response(serializer.data)

# Create Matiere
@api_view(['POST'])
def create_matiere(request):
    if request.method == 'POST':
        serializer = MatiereSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Matiere created successfully', 'id': serializer.data['id']}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Update Matiere (PUT)
@api_view(['PUT', 'DELETE'])
def update_matiere(request, pk):
    matiere = get_object_or_404(Matiere, pk=pk)
    if request.method == 'PUT':
        serializer = MatiereSerializer(matiere, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Matiere updated successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        matiere.delete()
        return Response({'message': 'Matiere deleted successfully'}, status=status.HTTP_200_OK)

# List Groupes
@api_view(['GET'])
def groupe_list(request):
    groupes = Groupe.objects.all()
    serializer = GroupeSerializer(groupes, many=True)
    return Response(serializer.data)

# Create Groupe
@api_view(['POST'])
def create_groupe(request):
    if request.method == 'POST':
        serializer = GroupeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Groupe created successfully', 'id': serializer.data['id']}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Update Groupe (PUT)
@api_view(['PUT', 'DELETE'])
def update_groupe(request, pk):
    groupe = get_object_or_404(Groupe, pk=pk)
    if request.method == 'PUT':
        serializer = GroupeSerializer(groupe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Groupe updated successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        groupe.delete()
        return Response({'message': 'Groupe deleted successfully'}, status=status.HTTP_200_OK)

# Assign Matiere to Groupe
@api_view(['POST'])
def assign_matiere_groupe(request):
    if request.method == 'POST':
        data = request.data
        groupe = get_object_or_404(Groupe, pk=data['groupe_id'])
        matiere = get_object_or_404(Matiere, pk=data['matiere_id'])

        MatiereGroupe.objects.create(groupe=groupe, matiere=matiere)
        return Response({'message': 'Matiere assigned to Groupe successfully'}, status=status.HTTP_200_OK)

# Delete Matiere-Groupe association
@api_view(['DELETE'])
def delete_matiere_groupe(request, pk):
    matiere_groupe = get_object_or_404(MatiereGroupe, pk=pk)
    matiere_groupe.delete()
    return Response({'message': 'Matiere-Groupe association deleted successfully'}, status=status.HTTP_200_OK)

# Assign Teacher to Matiere
@api_view(['POST'])
def assign_teacher_matiere(request):
    if request.method == 'POST':
        data = request.data
        teacher = get_object_or_404(Enseignant, pk=data['teacher_id'])
        matiere = get_object_or_404(Matiere, pk=data['matiere_id'])

        MatiereEnseignant.objects.create(enseignant=teacher, matiere=matiere)
        return Response({'message': 'Teacher assigned to Matiere successfully'}, status=status.HTTP_200_OK)

# Assign Teacher to Groupe
@api_view(['POST'])
def assign_teacher_groupe(request):
    if request.method == 'POST':
        data = request.data
        teacher = get_object_or_404(Enseignant, pk=data['teacher_id'])
        groupe = get_object_or_404(Groupe, pk=data['groupe_id'])

        TeacherGroupe.objects.create(enseignant=teacher, groupe=groupe)
        return Response({'message': 'Teacher assigned to Groupe successfully'}, status=status.HTTP_200_OK)

# Delete Teacher-Matiere association
@api_view(['DELETE'])
def delete_teacher_matiere(request, pk):
    teacher_matiere = get_object_or_404(MatiereEnseignant, pk=pk)
    teacher_matiere.delete()
    return Response({'message': 'Teacher-Matiere association deleted successfully'}, status=status.HTTP_200_OK)

# Delete Teacher-Groupe association
@api_view(['DELETE'])
def delete_teacher_groupe(request, pk):
    teacher_groupe = get_object_or_404(TeacherGroupe, pk=pk)
    teacher_groupe.delete()
    return Response({'message': 'Teacher-Groupe association deleted successfully'}, status=status.HTTP_200_OK)
