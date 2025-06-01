from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model

User = get_user_model

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password = None, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        elif not email:
            raise ValueError("Email is required")
        
        user = self.model(username = username, email = email, **extra_fields)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(username, email, password, **extra_fields)