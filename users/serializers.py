from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = ['id', 'username','password', 'role','email']
 
    def get_username (self, obj):
        return obj.username if  obj.username else obj.first_name
