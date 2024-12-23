from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='profile/%Y/%m/%d', verbose_name="Profile Image", blank=True)
    phone = models.CharField(max_length=11, verbose_name="Telfon raqami", blank=True)
    is_download = models.BooleanField(default=False, verbose_name="Yuklash")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kiritilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Uzgargan vaqti")
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"



# Bo'limlar uchun model
class Department(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name="department",
                                      blank=True, verbose_name="Foydalanuvchi")
    name = models.CharField(max_length=50, unique=True, null=False, blank=False, verbose_name="Nomi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kiritilgan vaqti")

    def __str__(self):
        return f"{self.user} -- {self.name}"

    class Meta:
        verbose_name = "Bo'lim"
        verbose_name_plural = "Bo'limlar"


# Lavozim modeli
class Position(models.Model):
    name = models.CharField(max_length=50, unique=False, null=False, blank=False, verbose_name="Nomi")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bo'lim")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kiritilgan vaqti")
    def __str__(self):
        return f"{self.department} - {self.name}"
    class Meta:
        verbose_name = "Lavozim"
        verbose_name_plural = "Lavozimlar"


# Ruxsatlar modelini yaratamiz (bu model lavozimga ko'ra metodlarga ruxsat beradi)
class Permission(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True,
                                related_name="user_permission", verbose_name="Foydalanuvchi", )
    position = models.OneToOneField(Position, on_delete=models.SET_NULL, related_name='permission',
                                    null=True, blank=True, verbose_name="Lavozim")
    can_get = models.BooleanField(default=False, verbose_name="GET")
    can_post = models.BooleanField(default=False, verbose_name="POST")
    can_patch = models.BooleanField(default=False, verbose_name="PATCH")
    can_put = models.BooleanField(default=False, verbose_name="PUT")
    can_delete = models.BooleanField(default=False, verbose_name="DELETE")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kiritilgan vaqti")
    def __str__(self):
        return f"Ruxsatnomalar uchun -{self.user} -- {self.position.name}"

    class Meta:
        verbose_name = "Ruxsat"
        verbose_name_plural = "Ruxsatnomalar"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True,
                                related_name="profile", verbose_name="Foydalanuvchi",)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bo'lim")
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Lavozim")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kiritilgan vaqti")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"


