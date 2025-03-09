from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.models import Permission
from django.core.validators import RegexValidator
class User(AbstractUser):
    ROLES_CHOICES = [
        ('admin', 'Admin'),
        ('enseignant', 'Enseignant'),
    ]
    role = models.CharField(max_length=20, choices=ROLES_CHOICES)
    email = models.CharField(max_length=255)
    USERNAME_FIELD = 'username'
    def __str__(self):
        return f"{self.email}"

    class Meta:
        permissions = [
            ("can_view_users", "Can view users"),
            ("can_edit_users", "Can edit users"),
            ("can_manage_users", "Can manage users"),
        ]
    def get_username(self, obj):
        return obj.get_username()

