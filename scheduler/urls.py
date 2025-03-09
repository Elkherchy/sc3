from django.urls import path
from .views import *

urlpatterns = [
    # Subjects (Matieres)
    path('matieres/', MatiereListCreateView.as_view(), name='matieres-list-create'),
    path('matieres/<int:pk>/', MatiereRetrieveUpdateDestroyView.as_view(), name='matieres-detail'),

    # Groups (Groupes)
    path('groupes/', GroupeListCreateView.as_view(), name='groupes-list-create'),
    path('groupes/<int:pk>/', GroupeRetrieveUpdateDestroyView.as_view(), name='groupes-detail'),

    # Teacher-Subject Relationship
    path('matiere-teachers/', MatiereTeacherListCreateView.as_view(), name='matiere-teacher-list-create'),
    path('matiere-teachers/<int:pk>/', MatiereTeacherRetrieveUpdateDestroyView.as_view(), name='matiere-teacher-detail'),

    # Teacher Availability
    path('disponibilites/', DisponibiliteEnseignantListCreateView.as_view(), name='disponibilite-list-create'),
    path('disponibilites/<int:pk>/', DisponibiliteEnseignantRetrieveUpdateDestroyView.as_view(), name='disponibilite-detail'),

    # Weekly Schedule
    path('planning/', PlanningHebdomadaireListCreateView.as_view(), name='planning-list-create'),
    path('planning/<int:pk>/', PlanningHebdomadaireRetrieveUpdateDestroyView.as_view(), name='planning-detail'),

    # Automatic Timetable Generation
     path('generate-schedule/', generate_schedule_api, name='generate-schedule'),
    path('set-fixed-schedule/', set_fixed_schedule, name='set-fixed-schedule'),

    # Export Schedule
    path('export-schedule-excel/', export_schedule_excel, name='export-schedule-excel'),
]
