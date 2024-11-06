from rest_framework.exceptions import PermissionDenied


def check_user_permissions(request, user, method):
    if not hasattr(user, 'profile') or not user.profile.position:
        raise PermissionDenied("Foydalanuvchi uchun lavozimlar belgilanmagan")

    permissions = user.profile.position.permission
    if method == 'GET' and not permissions.can_get:
        raise PermissionDenied("GET so'rovi uchun ruxsat yo'q..")