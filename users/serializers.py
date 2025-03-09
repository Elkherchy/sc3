from rest_framework import serializers
from scheduler.models import TeacherGroupe, MatiereTeacher , Matiere , Groupe
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    matieres = serializers.SerializerMethodField()
    groupes = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username','password', 'role','email', 'matieres', 'groupes']
    def get_groupes(self, obj):
        return list(
            Groupe.objects.filter(
                groupe_id__in=TeacherGroupe.objects.filter(enseignant=obj).values_list("groupe", flat=True)
            ).values_list("nom_groupe", flat=True)  # ✅ Récupérer le nom du groupe
        )

    def get_matieres(self, obj):
        return list(
            Matiere.objects.filter(
                matiere_id__in=MatiereTeacher.objects.filter(enseignant=obj).values_list("matiere", flat=True)
            ).values_list("nom_matiere", flat=True)  # ✅ Récupérer le nom de la matière
        )
    def get_username (self, obj):
        return obj.username if  obj.username else obj.first_name