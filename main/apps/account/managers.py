from django.contrib.auth.base_user import BaseUserManager
from ..common.manager import BaseManager


class UserManager(BaseUserManager, BaseManager):
    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone number must be set")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)
    

    def create_moderator(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_moderator", True)

        if extra_fields.get("is_moderator") is not True:
            raise ValueError("Moderator must have is_moderator=True.")

        return self._create_user(phone_number, password, **extra_fields)
    

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_moderator", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(phone_number, password, **extra_fields)
    

    def get_or_create(self, phone_number, password, **kwargs):
        try:
            instance = self.model.objects.get(phone_number=phone_number)
            return instance, False
        except self.model.DoesNotExist:
            instance = self.model.objects.create_user(
                phone_number=phone_number, password=password, **kwargs
            )
            return instance, True

    
