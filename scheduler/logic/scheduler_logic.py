from ortools.linear_solver import pywraplp
from scheduler.models import (
    PlanningHebdomadaire, ChargeHebdomadaire, DisponibiliteEnseignant,
    Groupe, Matiere, MatiereTeacher, TeacherGroupe
)
from django.db import transaction

def generate_schedule():
    """
    Uses OR-Tools to generate a conflict-free timetable
    based on teacher availability and subject-group relationships.
    """

    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return False, "Solver not available"

    # Load all necessary data from the database
    groupes = list(Groupe.objects.all())  # Get all student groups
    matieres = list(Matiere.objects.all())  # Get all subjects
    teacher_assignments = list(MatiereTeacher.objects.all())  # Teacher-Subject mapping
    teacher_group_assignments = list(TeacherGroupe.objects.all())  # Teacher-Group mapping
    disponibilites = list(DisponibiliteEnseignant.objects.all())  # Teacher Availabilities

    # Define time slots (Monday-Saturday, 5 slots per day)
    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
    slots = [1, 2, 3, 4, 5]

    # Create decision variables: X[g][m][d][t] (1 if group g has subject m at day d, slot t)
    X = {}
    for g in groupes:
        for m in matieres:
            for d in days:
                for t in slots:
                    X[(g.id, m.id, d, t)] = solver.BoolVar(f'X_{g.id}_{m.id}_{d}_{t}')

    # Constraint 1: Each subject must be scheduled for a group
    for g in groupes:
        for m in matieres:
            solver.Add(sum(X[g.id, m.id, d, t] for d in days for t in slots) == 1)

    # Constraint 2: No group can have two subjects at the same time
    for g in groupes:
        for d in days:
            for t in slots:
                solver.Add(sum(X[g.id, m.id, d, t] for m in matieres) <= 1)

    # Constraint 3: Teachers must be available before being assigned
    for disp in disponibilites:
        for g in groupes:
            for m in matieres:
                if MatiereTeacher.objects.filter(enseignant=disp.enseignant, matiere=m).exists():
                    solver.Add(X[g.id, m.id, disp.jour_semaine, disp.creneau_horaire] <= 1)

    # Constraint 4: One teacher cannot teach two groups at the same time
    for t in teacher_assignments:
        for d in days:
            for s in slots:
                solver.Add(sum(X[g.id, t.matiere.id, d, s] for g in groupes) <= 1)

    # Solve the optimization problem
    status = solver.Solve()

    # Handle full or partial solutions
    scheduled_classes = 0
    with transaction.atomic():
        PlanningHebdomadaire.objects.all().delete()  # Clear previous schedules
        for (g_id, m_id, d, t), var in X.items():
            if var.solution_value() == 1:
                teacher = MatiereTeacher.objects.filter(matiere_id=m_id).first().enseignant
                PlanningHebdomadaire.objects.create(
                    groupe_id=g_id,
                    matiere_id=m_id,
                    enseignant=teacher,
                    jour_semaine=d,
                    creneau_horaire=t,
                    type_lecon="CM"  # Default to CM
                )
                scheduled_classes += 1

    if status == pywraplp.Solver.OPTIMAL:
        return True, "Full schedule successfully generated"
    elif scheduled_classes > 0:
        return True, f"Partial schedule created: {scheduled_classes} classes placed"
    else:
        return False, "No feasible solution found"
