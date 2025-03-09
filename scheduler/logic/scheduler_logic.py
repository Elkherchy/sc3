from ortools.linear_solver import pywraplp
from scheduler.models import (
    FixedSchedule, PlanningHebdomadaire, ChargeHebdomadaire, DisponibiliteEnseignant,
    Groupe, Matiere, MatiereTeacher, TeacherGroupe, GroupeMatiere
)
from django.db import transaction

def generate_schedule():
    """
    Uses OR-Tools to generate a conflict-free timetable
    based on teacher availability, subject-group relationships, and constraints.
    """
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return False, "❌ Solver not available"

    # 📌 Load all necessary data from the database
    groupes = list(Groupe.objects.all())  
    matieres = list(Matiere.objects.all())  
    teacher_assignments = list(MatiereTeacher.objects.all())  
    teacher_group_assignments = list(TeacherGroupe.objects.all())  
    disponibilites = list(DisponibiliteEnseignant.objects.all())  
    course_loads = list(ChargeHebdomadaire.objects.all())  
    fixed_schedules = list(FixedSchedule.objects.all())  

    # 📅 Define available time slots (Monday-Saturday, 5 slots per day)
    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
    slots = [1, 2, 3, 4, 5]

    # ✅ Create decision variables: X[g][m][d][t] (1 if group g has subject m at day d, slot t)
    X = {}
    for g in groupes:
        for m in matieres:
            for d in days:
                for t in slots:
                    X[(g.groupe_id, m.matiere_id, d, t)] = solver.BoolVar(f'X_{g.groupe_id}_{m.matiere_id}_{d}_{t}')

    # 🔹 Constraint 1: Each required subject must be scheduled for a group
    for c in course_loads:
        solver.Add(sum(X[c.groupe.groupe_id, c.matiere.matiere_id, d, t] for d in days for t in slots) == 
                   (c.heures_cm + c.heures_td + c.heures_tp))

    # 🔹 Constraint 2: No group can have multiple subjects at the same time
    for g in groupes:
        for d in days:
            for t in slots:
                solver.Add(sum(X[g.groupe_id, m.matiere_id, d, t] for m in matieres) <= 1)

    # 🔹 Constraint 3: Teachers must be available before being assigned
    for disp in disponibilites:
        for tg in teacher_group_assignments:
            for m in matieres:
                if MatiereTeacher.objects.filter(enseignant=disp.enseignant, matiere=m).exists():
                    solver.Add(X[tg.groupe.groupe_id, m.matiere_id, disp.jour_semaine, disp.creneau_horaire] <= 1)

    # 🔹 Constraint 4: One teacher cannot teach two different groups at the same time
    for t in teacher_assignments:
        for d in days:
            for s in slots:
                solver.Add(sum(X[g.groupe_id, t.matiere.matiere_id, d, s] for g in groupes) <= 1)

    # 🔹 Constraint 5: Respect Fixed Schedules
    for fs in fixed_schedules:
        solver.Add(X[fs.groupe.groupe_id, fs.matiere.matiere_id, fs.jour_semaine, fs.creneau_horaire] == 1)

    print("🔄 Generating schedule...")
    status = solver.Solve()

    print("⚡ Solver Status:", status)
    if status == pywraplp.Solver.OPTIMAL:
        print("✅ Optimal solution found.")
    elif status == pywraplp.Solver.FEASIBLE:
        print("⚠️ Feasible but not optimal solution found.")
    else:
        print("❌ No solution found.")

    # 🔍 Debugging: Check which classes are being scheduled
    scheduled_classes = 0
    for (g_id, m_id, d, t), var in X.items():
        if var.solution_value() == 1:
            print(f"📅 Scheduled: Group {g_id}, Subject {m_id}, Day {d}, Slot {t}")
            scheduled_classes += 1

    print(f"📊 Total scheduled classes: {scheduled_classes}")

    # 🔄 Save schedule to database
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
                    type_lecon="CM"
                )

    if status == pywraplp.Solver.OPTIMAL:
        return True, "✅ Full schedule successfully generated"
    elif scheduled_classes > 0:
        return True, f"⚠️ Partial schedule created: {scheduled_classes} classes placed"
    else:
        return False, "❌ No feasible solution found"
