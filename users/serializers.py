from rest_framework import serializers
from scheduler.models import TeacherGroupe, MatiereTeacher
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    matieres = serializers.SerializerMethodField()
    groupes = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username','password', 'role','email', 'matieres', 'groupes']
    def get_groupes(self, obj):
        return TeacherGroupe.objects.filter(enseignant=obj).values_list("groupe", flat=True)

    def get_matieres(self, obj):
        return MatiereTeacher.objects.filter(enseignant=obj).values_list("matiere", flat=True)
    def get_username (self, obj):
        return obj.username if  obj.username else obj.first_name
