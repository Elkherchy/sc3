from ortools.linear_solver import pywraplp
from scheduler.models import (
    PlanningHebdomadaire, ChargeHebdomadaire, DisponibiliteEnseignant,
    Groupe, Matiere, MatiereTeacher, TeacherGroupe, ExceptionsPlanning
)
from django.db import transaction

def generate_schedule():
    """
    Uses OR-Tools to generate an automatic timetable based on database data.
    """

    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return False, "Solver not available"

    # Load all necessary data from the database
    groupes = list(Groupe.objects.all())
    matieres = list(Matiere.objects.all())
    teachers = list(MatiereTeacher.objects.all())
    disponibilites = list(DisponibiliteEnseignant.objects.all())
    charges = list(ChargeHebdomadaire.objects.all())
    exceptions = list(ExceptionsPlanning.objects.all())

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

    # Constraint 1: Each subject must be scheduled as per required weekly hours
    for ch in charges:
        solver.Add(sum(X[ch.groupe.id, ch.matiere.id, d, t] for d in days for t in slots) ==
                   (ch.heures_cm + ch.heures_td + ch.heures_tp))

    # Constraint 2: No group can have two subjects at the same time
    for g in groupes:
        for d in days:
            for t in slots:
                solver.Add(sum(X[g.id, m.id, d, t] for m in matieres) <= 1)

    # Constraint 3: Teachers' availability
    for disp in disponibilites:
        solver.Add(sum(X[g.id, m.id, disp.jour_semaine, disp.creneau_horaire] 
                       for g in groupes for m in matieres 
                       if MatiereTeacher.objects.filter(enseignant=disp.enseignant, matiere=m).exists()) <= 1)

    # Constraint 4: One teacher cannot teach two groups at the same time
    for t in teachers:
        for d in days:
            for s in slots:
                solver.Add(sum(X[g.id, t.matiere.id, d, s] for g in groupes) <= 1)

    # Constraint 5: Apply exceptions (manual scheduling)
    for ex in exceptions:
        if ex.type_exception == "suppression":
            solver.Add(X[ex.groupe.id, ex.matiere.id, ex.jour_semaine, ex.creneau_horaire] == 0)
        elif ex.type_exception == "ajout":
            solver.Add(X[ex.groupe.id, ex.matiere.id, ex.jour_semaine, ex.creneau_horaire] == 1)

    # Solve the optimization problem
    status = solver.Solve()

    # Handle full or partial solutions
    scheduled_classes = 0
    with transaction.atomic():
        PlanningHebdomadaire.objects.all().delete()  # Clear previous schedules
        for (g_id, m_id, d, t), var in X.items():
            if var.solution_value() == 1:
                PlanningHebdomadaire.objects.create(
                    groupe_id=g_id,
                    matiere_id=m_id,
                    enseignant=MatiereTeacher.objects.get(matiere_id=m_id).enseignant,
                    jour_semaine=d,
                    creneau_horaire=t,
                    type_lecon="CM"  # Default to CM, can be refined
                )
                scheduled_classes += 1

    if status == pywraplp.Solver.OPTIMAL:
        return True, "Full schedule successfully generated"
    elif scheduled_classes > 0:
        return True, f"Partial schedule created: {scheduled_classes} classes placed"
    else:
        return False, "No feasible solution found"
