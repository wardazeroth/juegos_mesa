from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

class UsuariosOnlineMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            cache_key = f"online_user_{request.user.id}"
            cache.set(cache_key, request.user.username, 300)
        return None