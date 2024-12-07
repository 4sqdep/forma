from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin  # Agar Django 2.x yoki undan oldin
import jwt


class TokenIPAndUserAgentCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Faqat autentifikatsiyalangan so'rovlar uchun tekshirish
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                # Tokenni dekodlash
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"], options={"verify_exp": True})

                # Token ichidan saqlangan IP va user-agentni olish
                token_ip = payload.get('ip_address')
                token_user_agent = payload.get('user_agent')

                # Joriy so'rovdagi IP va user-agentni olish
                current_ip = request.META.get('REMOTE_ADDR')

                # Agar proxy orqali so'rov kelsa, asl IPni olish
                if 'HTTP_X_FORWARDED_FOR' in request.META:
                    current_ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]

                current_user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')

                # Tekshirish: agar IP yoki user-agent mos kelmasa, rad etish
                if token_ip != current_ip or token_user_agent != current_user_agent:
                    raise PermissionDenied("Noto'g'ri IP manzil yoki qurilma orqali kirish.")

            except jwt.ExpiredSignatureError:
                raise PermissionDenied("Token muddati tugagan.")

            except jwt.InvalidTokenError:
                raise PermissionDenied("Yaroqsiz token.")

            except jwt.DecodeError:
                raise PermissionDenied("Tokenni dekodlashda xatolik.")

            except Exception as e:
                raise PermissionDenied(f"Xatolik yuz berdi: {str(e)}")


