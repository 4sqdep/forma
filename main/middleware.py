from django.utils.deprecation import MiddlewareMixin


class AllowIframeMiddleware(MiddlewareMixin):
    def process_request(self, request, response):
        response['X-Frame-Options'] = 'ALLOWALL' # Hamma domenlarga ruxsat berish
        return response
