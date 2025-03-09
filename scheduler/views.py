from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from scheduler.logic.scheduler_logic import generate_schedule
from django.contrib.auth.decorators import login_required

# ✅ CRUD for Subjects (Matieres)
class MatiereListCreateView(generics.ListCreateAPIView):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer
    permission_classes = [AllowAny]

class MatiereRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer
    permission_classes = [AllowAny]

# ✅ CRUD for Groups (Groupes)
class GroupeListCreateView(generics.ListCreateAPIView):
    queryset = Groupe.objects.all()
    serializer_class = GroupeSerializer
    permission_classes = [AllowAny]

class GroupeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Groupe.objects.all()
    serializer_class = GroupeSerializer
    permission_classes = [AllowAny]

# ✅ CRUD for Teacher-Subject Relationship (MatiereTeacher)
class MatiereTeacherListCreateView(generics.ListCreateAPIView):
    queryset = MatiereTeacher.objects.all()
    serializer_class = MatiereTeacherSerializer
    permission_classes = [AllowAny]

class MatiereTeacherRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MatiereTeacher.objects.all()
    serializer_class = MatiereTeacherSerializer
    permission_classes = [AllowAny]

# ✅ CRUD for Teacher Availability (DisponibiliteEnseignant)
class DisponibiliteEnseignantListCreateView(generics.ListCreateAPIView):
    queryset = DisponibiliteEnseignant.objects.all()
    serializer_class = DisponibiliteEnseignantSerializer
    permission_classes = [AllowAny]

class DisponibiliteEnseignantRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DisponibiliteEnseignant.objects.all()
    serializer_class = DisponibiliteEnseignantSerializer
    permission_classes = [AllowAny]

# ✅ CRUD for Weekly Schedule (PlanningHebdomadaire)
class PlanningHebdomadaireListCreateView(generics.ListCreateAPIView):
    queryset = PlanningHebdomadaire.objects.all()
    serializer_class = PlanningHebdomadaireSerializer
    permission_classes = [AllowAny]

class PlanningHebdomadaireRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlanningHebdomadaire.objects.all()
    serializer_class = PlanningHebdomadaireSerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
@permission_classes([AllowAny])
def generate_schedule_api(request):
    """
    API endpoint to generate the automatic schedule.
    """
    success, message = generate_schedule()
    if success:
        return Response({"status": "success", "message": message}, status=status.HTTP_201_CREATED)
    else:
        return Response({"status": "error", "message": message}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def set_fixed_schedule(request):
    """
    API endpoint to manually set a class at a specific time slot.
    """
    from scheduler.models import PlanningHebdomadaire
    try:
        data = request.data
        PlanningHebdomadaire.objects.create(
            groupe_id=data["groupe_id"],
            matiere_id=data["matiere_id"],
            enseignant_id=data["enseignant_id"],
            jour_semaine=data["jour_semaine"],
            creneau_horaire=data["creneau_horaire"],
            type_lecon="CM"
        )
        return Response({"status": "success", "message": "Class fixed successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([AllowAny])
def export_schedule_excel(request):
    import pandas as pd
    from django.http import HttpResponse

    schedules = PlanningHebdomadaire.objects.all().values('groupe__nom_groupe', 'matiere__nom_matiere', 'enseignant__username', 'jour_semaine', 'creneau_horaire')
    df = pd.DataFrame(schedules)
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=schedule.xlsx'
    df.to_excel(response, index=False)
    return response