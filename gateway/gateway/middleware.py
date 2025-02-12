from django.http import JsonResponse
from django.conf import settings
from .auth_producer import AuthProducer

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.paths_to_protect = settings.PROTECTED_ROUTES
        self.auth = AuthProducer()

    def __call__(self, request):
        if request.path.startswith('/api'):
            request.path = request.path[4:]
            
        if request.path in self.paths_to_protect:
            token = request.headers.get('Authorization')
            if not token:
                return JsonResponse({'error': 'Missing token'}, status=401)

            user = self.auth.check_auth(token)
            if not user or not user.get('is_authenticated'):
                return JsonResponse({"error": "Authentication not provided"}, status=401)

            request.user_id = user["user_id"]

        return self.get_response(request)