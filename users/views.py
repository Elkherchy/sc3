from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import Group, Permission
from users.models import User
from users.serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.exceptions import TokenError
from users.utils import generate_password, send_password_email  

class UserListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                'error': 'Username and password are required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        print(f"Received credentials: username={username}, password={password}")

        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response({

                'refresh': str(refresh),
                'access': str(access_token),
                'id':user.id,
                'username': user.username,
                'role': user.role,
                'email': user.email,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'username': username,
                'password': password,
                'error': 'Invalid credentials'
                
            }, status=status.HTTP_401_UNAUTHORIZED)
class CreateEnseignantView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Création ou récupération des groupes et permissions
            admin_group, _ = Group.objects.get_or_create(name='Admin')
            enseignant_group, _ = Group.objects.get_or_create(name='Enseignant')

            permission_view_users, _ = Permission.objects.get_or_create(
                codename='can_view_users', name='Can view users'
            )
            permission_edit_users, _ = Permission.objects.get_or_create(
                codename='can_edit_users', name='Can edit users'
            )

            admin_group.permissions.add(permission_view_users, permission_edit_users)
            enseignant_group.permissions.add(permission_view_users)

            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                # Sauvegarde initiale de l'utilisateur
                user = serializer.save()
                # Générer un mot de passe et le définir
                password_code = generate_password()
                user.set_password(password_code)
                user.save()

                # Attribution des groupes en fonction du rôle
                role = user.role.lower()
                if role == 'admin':
                    user.groups.add(admin_group)
                elif role == 'enseignant':
                    user.groups.add(enseignant_group)

                # Envoi du mot de passe par email
                send_password_email(user.email, password_code)

                return Response({
                    "message": "User created and groups, permissions assigned successfully"
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "error": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


        

class LogoutView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, TokenError):
            return Response(status=status.HTTP_400_BAD_REQUEST)