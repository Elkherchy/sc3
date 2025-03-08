# urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Enseignant URLs
    path('enseignants/', views.enseignant_list, name='enseignant_list'),
    path('enseignants/create/', views.create_enseignant, name='create_enseignant'),
    path('enseignants/update/<int:pk>/', views.update_enseignant, name='update_enseignant'),

    # Matiere URLs
    path('matieres/', views.matiere_list, name='matiere_list'),
    path('matieres/create/', views.create_matiere, name='create_matiere'),
    path('matieres/update/<int:pk>/', views.update_matiere, name='update_matiere'),

    # Groupe URLs
    path('groupes/', views.groupe_list, name='groupe_list'),
    path('groupes/create/', views.create_groupe, name='create_groupe'),
    path('groupes/update/<int:pk>/', views.update_groupe, name='update_groupe'),

    # Assignment URLs
    path('assign_matiere_groupe/', views.assign_matiere_groupe, name='assign_matiere_groupe'),
    path('delete_matiere_groupe/<int:pk>/', views.delete_matiere_groupe, name='delete_matiere_groupe'),
    path('assign_teacher_matiere/', views.assign_teacher_matiere, name='assign_teacher_matiere'),
    path('assign_teacher_groupe/', views.assign_teacher_groupe, name='assign_teacher_groupe'),
    path('delete_teacher_matiere/<int:pk>/', views.delete_teacher_matiere, name='delete_teacher_matiere'),
    path('delete_teacher_groupe/<int:pk>/', views.delete_teacher_groupe, name='delete_teacher_groupe'),
]
