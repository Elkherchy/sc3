from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt



from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from scheduler.models import PlanningHebdomadaire
from datetime import date, timedelta
from scheduler.logic.scheduler_logic import generate_schedule
from django.contrib.auth.decorators import login_required
# ✅ CRUD for Calendrier (Time Slots)

class FullCalendrierView(APIView):
    permission_classes = [AllowAny]  # ✅ Allow access without authentication

    def get(self, request):
        # Define default calendar
        JOURS_SEMAINE = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
        CRENEAUX_HORAIRES = {
            1: "08h00 - 09h30",
            2: "09h45 - 11h15",
            3: "11h30 - 13h00",
            4: "15h00 - 16h30",
            5: "17h00 - 18h30"
        }

        # Get all exceptions from database
        exceptions = CalendrierException.objects.all()
        exceptions_dict = {(e.jour_semaine, e.creneau_horaire, e.date): e for e in exceptions}

        # Build full calendar response
        full_calendar = []
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())  # Get Monday of this week

        for i in range(6):  # Monday to Saturday
            day_name = JOURS_SEMAINE[i]
            for slot_id, slot_time in CRENEAUX_HORAIRES.items():
                exception_key = (day_name, slot_id, start_of_week)
                if exception_key in exceptions_dict:
                    # If there's an exception, apply it
                    exception = exceptions_dict[exception_key]
                    if exception.type_exception == "suppression":
                        continue  # Skip removed slots
                    elif exception.type_exception == "ajout":
                        full_calendar.append({
                            "jour_semaine": exception.jour_semaine,
                            "creneau_horaire": exception.creneau_horaire,
                            "creneau_horaire_display": CRENEAUX_HORAIRES[exception.creneau_horaire],
                            "type_exception": exception.type_exception,
                            "date": str(exception.date)
                        })
                else:
                    # Default time slots
                    full_calendar.append({
                        "jour_semaine": day_name,
                        "creneau_horaire": slot_id,
                        "creneau_horaire_display": slot_time,
                        "type_exception": "default",
                        "date": str(start_of_week)
                    })

        # Add any extra Sunday slots from exceptions
        for exception in exceptions:
            if exception.jour_semaine == "Dimanche":
                full_calendar.append({
                    "jour_semaine": exception.jour_semaine,
                    "creneau_horaire": exception.creneau_horaire,
                    "creneau_horaire_display": CRENEAUX_HORAIRES[exception.creneau_horaire],
                    "type_exception": exception.type_exception,
                    "date": str(exception.date)
                })

        return Response(full_calendar)


class CalendrierExceptionListCreateView(generics.ListCreateAPIView):
    queryset = CalendrierException.objects.all()
    serializer_class = CalendrierExceptionSerializer
    permission_classes = [AllowAny]

class FixedScheduleListCreateView(generics.ListCreateAPIView):
    queryset = FixedSchedule.objects.all()
    serializer_class = FixedScheduleSerializer
    permission_classes = [AllowAny]

class CalendrierExceptionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CalendrierException.objects.all()
    serializer_class = CalendrierExceptionSerializer
    permission_classes = [AllowAny]
# ✅ CRUD for Charge Hebdomadaire (Weekly Workload)

class ChargeHebdomadaireListCreateView(generics.ListCreateAPIView):
    queryset = ChargeHebdomadaire.objects.all()
    serializer_class = ChargeHebdomadaireSerializer
    permission_classes = [AllowAny]


class ChargeHebdomadaireRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChargeHebdomadaire.objects.all()
    serializer_class = ChargeHebdomadaireSerializer
    permission_classes = [AllowAny]

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

# ✅ CRUD for Assigning Teacher to Subject (MatiereTeacher)

class MatiereTeacherListCreateView(generics.ListCreateAPIView):
    queryset = MatiereTeacher.objects.all()
    serializer_class = MatiereTeacherSerializer
    permission_classes = [AllowAny]

class MatiereTeacherRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MatiereTeacher.objects.all()
    serializer_class = MatiereTeacherSerializer
    permission_classes = [AllowAny]

# ✅ CRUD for Assigning Subject to Group (GroupeMatiere)

class GroupeMatiereListCreateView(generics.ListCreateAPIView):
    queryset = GroupeMatiere.objects.all()
    serializer_class = GroupeMatiereSerializer
    permission_classes = [AllowAny]

class GroupeMatiereRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupeMatiere.objects.all()
    serializer_class = GroupeMatiereSerializer
    permission_classes = [AllowAny]

# ✅ CRUD for Assigning Teacher to Group (TeacherGroupe)

class TeacherGroupeListCreateView(generics.ListCreateAPIView):
    queryset = TeacherGroupe.objects.all()
    serializer_class = TeacherGroupeSerializer
    permission_classes = [AllowAny]

class TeacherGroupeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeacherGroupe.objects.all()
    serializer_class = TeacherGroupeSerializer
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


TIME_SLOTS = {
    1: "08:00 - 09:30",
    2: "09:45 - 11:15",
    3: "11:30 - 13:00",
    4: "15:00 - 16:30",
    5: "17:00 - 18:30"
}
DAYS_ORDER = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def generate_schedule_api(request):
    """
    Generates a schedule for a specific group and returns it directly in the response.
    """
    groupe_id = request.data.get("groupe")  # Get the requested group from POST data

    if not groupe_id:
        return Response({"status": "error", "message": "❌ Groupe ID is required."}, status=400)

    success, message = generate_schedule(groupe_id)  # ✅ Generate the schedule for the given group

    if not success:
        return Response({"status": "error", "message": message}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Fetch the generated schedule for the specific group from the database
    schedule = {day: [] for day in DAYS_ORDER}

    try:
        groupe = Groupe.objects.get(pk=groupe_id)  # Ensure correct ID lookup
    except Groupe.DoesNotExist:
        return Response({"status": "error", "message": "❌ Groupe not found."}, status=400)

    planning = PlanningHebdomadaire.objects.filter(groupe=groupe).select_related('matiere', 'enseignant')

    for entry in planning:
        schedule[entry.jour_semaine].append({
            "Heure": TIME_SLOTS.get(entry.creneau_horaire, "Unknown"),
            "Matière": entry.matiere.nom_matiere,
            "Type": entry.type_lecon,
            "Enseignant": entry.enseignant.username if entry.enseignant else "N/A"
        })

    return Response({
        "status": "success",
        "message": f"✅ Full schedule successfully generated for {groupe.nom_groupe}",
        "groupe": groupe.nom_groupe,
        "schedule": schedule  # Return the generated timetable directly
    }, status=status.HTTP_201_CREATED)
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def set_fixed_schedule(request):
    """
    API endpoint to manually set a class at a specific time slot.
    """
    try:
        data = request.data
        print("📌 Received data for fixed schedule:", data)  # Debugging

        # Convert values to integers
        groupe_id = int(data["groupe_id"])
        matiere_id = int(data["matiere_id"])
        enseignant_id = int(data["enseignant_id"])
        jour_semaine = data["jour_semaine"]
        creneau_horaire = int(data["creneau_horaire"])

        PlanningHebdomadaire.objects.create(
            groupe_id=groupe_id,
            matiere_id=matiere_id,
            enseignant_id=enseignant_id,
            jour_semaine=jour_semaine,
            creneau_horaire=creneau_horaire,
            type_lecon="CM"
        )

        return Response({"status": "success", "message": "✅ Class fixed successfully"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print("❌ Error in set_fixed_schedule:", str(e))  # Debugging
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
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
# Define time slots mapping
TIME_SLOTS = {
    1: "08:00 - 09:30",
    2: "09:45 - 11:15",
    3: "11:30 - 13:00",
    4: "15:00 - 16:30",
    5: "17:00 - 18:30"
}

DAYS_ORDER = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
@csrf_exempt
@api_view(['GET'])
def export_schedule_json(request, groupe_id):
    """
    Exports the schedule in a structured JSON format for a specific group.
    """
    groupe = get_object_or_404(Groupe, pk=groupe_id)  # Get the group or return 404
    schedule = {day: [] for day in DAYS_ORDER}  # Initialize empty schedule

    # Fetch all planned lessons for the specific group
    planning = PlanningHebdomadaire.objects.filter(groupe=groupe).select_related('matiere', 'enseignant')

    for entry in planning:
        schedule[entry.jour_semaine].append({
            "Heure": TIME_SLOTS.get(entry.creneau_horaire, "Unknown"),
            "Matière": entry.matiere.nom_matiere,
            "Type": entry.type_lecon,
            "Groupe": groupe.nom_groupe,  # Only one group now
            "Enseignant": entry.enseignant.username if entry.enseignant else "N/A"
        })

    return JsonResponse(schedule, safe=False)
