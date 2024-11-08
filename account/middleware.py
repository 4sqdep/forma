import jwt
from django.conf import settings
from rest_framework.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin


class TokenIPAndUserAgentCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Faqat autentifikatsiyalangan so'rovlar uchun tekshirish
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                # Token Dekod qilsih
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

                # Token ichidan saqlangan IP va user-agentni olish
                token_ip = payload.get('ip_address')
                token_user_agent = payload.get('user_agent')

                # Joriy so'rovdagi IP va user-agentni olish
                current_ip = request.META.get('REMOTE_ADDR')
                current_user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')

                # Tekshirish: agar IP yoki user-agent mos kelmasa, rad etish
                if token_ip != current_ip or token_user_agent != current_user_agent:
                    raise PermissionDenied("Noto'g'ri IP manzil yoki qurilma orqali kirish.")

            except jwt.ExpiredSignatureError:
                raise PermissionDenied("Token muddati tugagan.")

            except jwt.InvalidTokenError:
                raise PermissionDenied("Yaroqsiz token.")


