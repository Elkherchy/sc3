from django.urls import path
from .views import (
    calendrier_list_create, calendrier_detail, disponibilites_list_create, 
    disponibilites_detail, planning_list_create, planning_detail, charge_list_create, 
    exceptions_list_create
)

urlpatterns = [
    path('calendrier/', calendrier_list_create),
    path('calendrier/<int:pk>/', calendrier_detail),
    
    path('disponibilites/', disponibilites_list_create),
    path('disponibilites/<int:pk>/', disponibilites_detail),
    
    path('planning/', planning_list_create),
    path('planning/<int:pk>/', planning_detail),
    
    path('charge/', charge_list_create),
    
    path('exceptions/', exceptions_list_create),
]
