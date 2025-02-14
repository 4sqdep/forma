from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from main.apps.account.manager import UserManager
from main.apps.account.models.department import Department
from main.apps.account.models.position import Position
from main.apps.common.models import BaseMeta, BaseModel
from django.utils.translation import gettext_lazy as _
from main.apps.common.utils import upload_file




class User(AbstractUser, PermissionsMixin, BaseModel):
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    username = models.CharField(_("username"), max_length=150, unique=True)
    phone = models.CharField(max_length=14, verbose_name="Telfon raqami", blank=True)
    email = models.EmailField(null=True, blank=True)
    is_download = models.BooleanField(default=False, verbose_name="Yuklash")
    image = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site.",
        ),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting account."
        ),
    )
    is_moderator = models.BooleanField(_("moderator status"), default=False)
    is_superuser = models.BooleanField(_("superuser status"), default=False)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = "username"

    class Meta(BaseMeta):
        db_table = "user"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name}"




class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True,
                                related_name="profile", verbose_name="Foydalanuvchi",)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bo'lim")
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Lavozim")

    def __str__(self):
        return self.user.username
    
    class Meta(BaseMeta):
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"



# class Permission(models.Model):
#     user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True,
#                                 related_name="user_permission", verbose_name="Foydalanuvchi", )
#     position = models.OneToOneField(Position, on_delete=models.SET_NULL, related_name='permission',
#                                     null=True, blank=True, verbose_name="Lavozim")
#     can_get = models.BooleanField(default=False, verbose_name="GET")
#     can_post = models.BooleanField(default=False, verbose_name="POST")
#     can_patch = models.BooleanField(default=False, verbose_name="PATCH")
#     can_put = models.BooleanField(default=False, verbose_name="PUT")
#     can_delete = models.BooleanField(default=False, verbose_name="DELETE")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kiritilgan vaqti")
#     def __str__(self):
#         return f"Ruxsatnomalar uchun -{self.user} -- {self.position.name}"

#     class Meta:
#         verbose_name = "Ruxsat"
#         verbose_name_plural = "Ruxsatnomalar"
