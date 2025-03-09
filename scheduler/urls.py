from django.urls import path
from .views import *

urlpatterns = [
    # ✅ Subjects (Matieres)
    path('matieres/', MatiereListCreateView.as_view(), name='matieres-list-create'),
    path('matieres/<int:pk>/', MatiereRetrieveUpdateDestroyView.as_view(), name='matieres-detail'),

    # ✅ Groups (Groupes)
    path('groupes/', GroupeListCreateView.as_view(), name='groupes-list-create'),
    path('groupes/<int:pk>/', GroupeRetrieveUpdateDestroyView.as_view(), name='groupes-detail'),

    # ✅ Assign Teacher to Subject
    path('matiere-teachers/', MatiereTeacherListCreateView.as_view(), name='matiere-teacher-list-create'),
    path('matiere-teachers/<int:pk>/', MatiereTeacherRetrieveUpdateDestroyView.as_view(), name='matiere-teacher-detail'),

    # ✅ Assign Subject to Group
    path('groupe-matieres/', GroupeMatiereListCreateView.as_view(), name='groupe-matiere-list-create'),
    path('groupe-matieres/<int:pk>/', GroupeMatiereRetrieveUpdateDestroyView.as_view(), name='groupe-matiere-detail'),

    # ✅ Assign Teacher to Group
    path('teacher-groupes/', TeacherGroupeListCreateView.as_view(), name='teacher-groupe-list-create'),
    path('teacher-groupes/<int:pk>/', TeacherGroupeRetrieveUpdateDestroyView.as_view(), name='teacher-groupe-detail'),

    # ✅ Teacher Availability
    path('disponibilites/', DisponibiliteEnseignantListCreateView.as_view(), name='disponibilite-list-create'),
    path('disponibilites/<int:pk>/', DisponibiliteEnseignantRetrieveUpdateDestroyView.as_view(), name='disponibilite-detail'),

    # ✅ Weekly Schedule
    path('planning/', PlanningHebdomadaireListCreateView.as_view(), name='planning-list-create'),
    path('planning/<int:pk>/', PlanningHebdomadaireRetrieveUpdateDestroyView.as_view(), name='planning-detail'),
    path('set-fixed-schedule/', FixedScheduleListCreateView.as_view(), name='set-fixed-schedule'),
    # ✅ Automatic Timetable Generation
    path('generate-schedule/', generate_schedule_api, name='generate-schedule'),
    path('set-fixed-schedule/', set_fixed_schedule, name='set-fixed-schedule'),

    # ✅ Export Schedule
    path('export-schedule-excel/', export_schedule_excel, name='export-schedule-excel'),
    path('export-schedule/<int:groupe_id>/', export_schedule_json, name='export-schedule'),
     path('calendrier-exceptions/', CalendrierExceptionListCreateView.as_view(), name='calendrier-exception-list-create'),
    path('calendrier-exceptions/<int:pk>/', CalendrierExceptionRetrieveUpdateDestroyView.as_view(), name='calendrier-exception-detail'),
    path('calendrier/', FullCalendrierView.as_view(), name='full-calendrier'),


    # 📌 NEW: Weekly Workload Management (Charge Hebdomadaire)
    path('charge-hebdomadaire/', ChargeHebdomadaireListCreateView.as_view(), name='charge-list-create'),
    path('charge-hebdomadaire/<int:pk>/', ChargeHebdomadaireRetrieveUpdateDestroyView.as_view(), name='charge-detail'),
]
