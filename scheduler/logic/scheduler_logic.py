from ortools.linear_solver import pywraplp
from scheduler.models import (
    FixedSchedule, PlanningHebdomadaire, ChargeHebdomadaire, DisponibiliteEnseignant,
    Groupe, Matiere, MatiereTeacher, TeacherGroupe, GroupeMatiere
)
from django.db import transaction

# Define time slots mapping
TIME_SLOTS = {
    1: "08:00 - 09:30",
    2: "09:45 - 11:15",
    3: "11:30 - 13:00",
    4: "15:00 - 16:30",
    5: "17:00 - 18:30"
}

DAYS_ORDER = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]

def generate_schedule(groupe_id):
    """
    Uses OR-Tools to generate a conflict-free timetable for a specific group.
    """
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return False, "❌ Solver not available"

    print(f"🔄 Generating timetable for Groupe ID: {groupe_id}")

    # 📌 Load data for the given group
    try:
        groupe = Groupe.objects.get(groupe_id=groupe_id)
    except Groupe.DoesNotExist:
        return False, "❌ Groupe not found."

    matieres = list(GroupeMatiere.objects.filter(groupe=groupe).select_related("matiere"))
    teacher_assignments = list(MatiereTeacher.objects.all())  
    disponibilites = list(DisponibiliteEnseignant.objects.all())  
    course_loads = list(ChargeHebdomadaire.objects.filter(groupe=groupe))  
    fixed_schedules = list(FixedSchedule.objects.filter(groupe=groupe))  

    # ✅ Create decision variables: X[m][d][t] (1 if matiere m at day d, slot t)
    X = {}
    for gm in matieres:
        for d in DAYS_ORDER:
            for t in TIME_SLOTS.keys():
                X[(gm.matiere.matiere_id, d, t)] = solver.BoolVar(f'X_{gm.matiere.matiere_id}_{d}_{t}')

    # 🔹 Constraint 1: Ensure each subject is scheduled according to its weekly load
    for c in course_loads:
        matiere_id = c.matiere.matiere_id
        if any((matiere_id, d, t) in X for d in DAYS_ORDER for t in TIME_SLOTS.keys()):  
            solver.Add(sum(X[matiere_id, d, t] for d in DAYS_ORDER for t in TIME_SLOTS.keys() if (matiere_id, d, t) in X) == 
                       (c.heures_cm + c.heures_td + c.heures_tp))

    # 🔹 Constraint 2: Prevent scheduling two subjects at the same time for this group
    for d in DAYS_ORDER:
        for t in TIME_SLOTS.keys():
            if any((m.matiere.matiere_id, d, t) in X for m in matieres):
                solver.Add(sum(X[m.matiere.matiere_id, d, t] for m in matieres if (m.matiere.matiere_id, d, t) in X) <= 1)

    # 🔹 Constraint 3: Ensure teachers are available before being assigned
    for disp in disponibilites:
        for m in matieres:
            if MatiereTeacher.objects.filter(enseignant=disp.enseignant, matiere=m.matiere).exists():
                if (m.matiere.matiere_id, disp.jour_semaine, disp.creneau_horaire) in X:
                    solver.Add(X[m.matiere.matiere_id, disp.jour_semaine, disp.creneau_horaire] <= 1)

    # 🔹 Constraint 4: Prevent a teacher from teaching multiple groups at the same time
    for t in teacher_assignments:
        for d in DAYS_ORDER:
            for s in TIME_SLOTS.keys():
                if any((m.matiere.matiere_id, d, s) in X for m in matieres):
                    solver.Add(sum(X[m.matiere.matiere_id, d, s] for m in matieres if (m.matiere.matiere_id, d, s) in X) <= 1)

    # 🔹 Constraint 5: Respect Fixed Schedules
    for fs in fixed_schedules:
        if (fs.matiere.matiere_id, fs.jour_semaine, fs.creneau_horaire) in X:
            solver.Add(X[fs.matiere.matiere_id, fs.jour_semaine, fs.creneau_horaire] == 1)

    print("🔄 Solving the schedule...")
    status = solver.Solve()

    print("⚡ Solver Status:", status)
    if status == pywraplp.Solver.OPTIMAL:
        print("✅ Optimal solution found.")
    elif status == pywraplp.Solver.FEASIBLE:
        print("⚠️ Feasible but not optimal solution found.")
    else:
        print("❌ No solution found.")

    # 🔍 Save schedule to the database
    scheduled_classes = []
    with transaction.atomic():
        PlanningHebdomadaire.objects.filter(groupe=groupe).delete()  # Clear previous schedules
        for (m_id, d, t), var in X.items():
            if var.solution_value() == 1:
                teacher_assignment = MatiereTeacher.objects.filter(matiere_id=m_id).first()
                teacher = teacher_assignment.enseignant if teacher_assignment else None

            PlanningHebdomadaire.objects.create(
                groupe=groupe,
                matiere_id=m_id,
                enseignant=teacher,
                jour_semaine=d,
                creneau_horaire=t,  # Ensure this matches the time slot correctly
                type_lecon="CM"
            )

        scheduled_classes.append((m_id, d, t))

    if status == pywraplp.Solver.OPTIMAL:
        return True, "✅ Full schedule successfully generated"
    elif len(scheduled_classes) > 0:
        return True, f"⚠️ Partial schedule created: {len(scheduled_classes)} classes placed"
    else:
        return False, "❌ No feasible solution found"
