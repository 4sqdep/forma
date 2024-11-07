from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from account.models import UserProfile

class CanGetPermission(BasePermission):
    """
    Foydalanuvchida `can_get=True` ruxsati borligini tekshiradi.
    """
    def has_permission(self, request, view):
        # can_get ruxsati borligini tekshirish
        if request.method == "GET":
            if UserProfile.objects.filter(user=request.user, position__permission__can_get=True).exists():
                return True
            else:
                # Agar ruxsat yo'q bo'lsa, xabar bilan istisno chiqaradi
                raise PermissionDenied(detail="Ruxsat yo'q: Siz ushbu ma'lumotga kirish huquqiga ega emassiz.")
        elif request.method == "POST":
            if UserProfile.objects.filter(user=request.user, position__permission__can_post=True).exists():
                return True
            else:
                # Agar ruxsat yo'q bo'lsa, xabar bilan istisno chiqaradi
                raise PermissionDenied(detail="Ruxsat yo'q: Siz ushbu ma'lumotga kirish huquqiga ega emassiz.")
        elif request.method == "DELETE":
            if UserProfile.objects.filter(user=request.user, position__permission__can_delete=True).exists():
                return True
            else:
                # Agar ruxsat yo'q bo'lsa, xabar bilan istisno chiqaradi
                raise PermissionDenied(detail="Ruxsat yo'q: Siz ushbu ma'lumotga kirish huquqiga ega emassiz.")
        elif request.method == "PUT":
            if UserProfile.objects.filter(user=request.user, position__permission__can_put=True).exists():
                return True
            else:
                # Agar ruxsat yo'q bo'lsa, xabar bilan istisno chiqaradi
                raise PermissionDenied(detail="Ruxsat yo'q: Siz ushbu ma'lumotga kirish huquqiga ega emassiz.")
        elif request.method == "PATCH":
            if UserProfile.objects.filter(user=request.user, position__permission__can_patch=True).exists():
                return True
            else:
                # Agar ruxsat yo'q bo'lsa, xabar bilan istisno chiqaradi
                raise PermissionDenied(detail="Ruxsat yo'q: Siz ushbu ma'lumotga kirish huquqiga ega emassiz.")
        return False
