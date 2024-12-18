import os
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from main.apps.account.managers import UserManager
from main.apps.account.utils import otp_expire_time
from ..common.models import BaseModel, BaseMeta


def upload_profile_images(instance, filename):
    filename_without_extension, extension = os.path.splitext(filename.lower())
    timestamp = timezone.now().strftime("%Y-%m-%d.%H-%M-%S")
    filename = f"{slugify(filename_without_extension)}.{timestamp}{extension}"
    return f"profile/{filename}"


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    class PositionChoices(models.TextChoices):
        MANAGER = "manager"
        MODERATOR = "moderator"
        ASSISTANT = 'assistant'

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    middle_name = models.CharField(_("middle name"), max_length=150, blank=True)
    phone_number = models.CharField(max_length=255, unique=True,
                             verbose_name=_("Телефонный номер"))
    profile_picture = models.ImageField(
        upload_to=upload_profile_images,
        blank=True,
        null=True
    )
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
    date_of_birth = models.DateField(null=True, blank=True)
    position = models.CharField(
        choices=PositionChoices.choices,
        max_length=15,
    )
    passport_series = models.CharField(max_length=255, null=True, blank=True)
    is_moderator = models.BooleanField(_("moderator status"), default=False)
    is_superuser = models.BooleanField(_("superuser status"), default=False)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    activating_code = models.CharField(max_length=50, null=True)
    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    class Meta:
        ordering = ("-id",)
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



class ActivationSMSCode(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sms', null=True)
    otp = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    is_verified = models.BooleanField(default=False)
    otp_sent_time = models.CharField(max_length=100,null=True, blank=True, default=otp_expire_time)
    otp_sent_time_reset = models.CharField(max_length=100,null=True, blank=True)


    def __str__(self):
        return self.phone_number

    class Meta(BaseMeta):
        verbose_name_plural = "ActivationSMSCodes"
        ordering = ['-id']