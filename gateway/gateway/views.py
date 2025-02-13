import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

def get_service_url(path):
    for route, url in settings.SERVICE_ROUTES.items():
        if path.startswith(route):
            return url
    return None

class APIGatewayView(APIView):

    def operations(self, request, path):
        headers = dict(request.headers)

        if request.path in settings.PROTECTED_ROUTES:
            headers['id'] = str(request.user_id)
        
        base_url = get_service_url(request.path)
        if not base_url:
            return Response({'error': 'Invalid path'}, status=status.HTTP_404_NOT_FOUND)

        full_url = f"{base_url}/{path}?format=json"
        params = request.query_params
        if params:
            full_url += f"&{params.urlencode()}"
        method = request.method.lower()
        print(f"full_url : {full_url}")
        try:
            response = requests.request(method, full_url, headers=headers, json=request.data)
            if response.status_code == 404:
                print(f"Not found : {full_url}")
                return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.RequestException as e:
            print(f"Error in request: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if response.headers.get('content-type') == 'application/json':
            return Response(response.json(), status=response.status_code)
        return Response(response.content, status=response.status_code)
    
    def get_ratelimit_key(self, request):
        return str(request.user_id) if hasattr(request, "user_id") else request.META.get("REMOTE_ADDR")
    
    def get_ratelimit_rate(self, request):
        return "300/h" if hasattr(request, "user_id") else "100/h"
        
    @method_decorator(ratelimit(key=get_ratelimit_key, rate=get_ratelimit_rate, method='GET', block=True))
    def get(self, request, path):
        return self.operations(request, path)

    @method_decorator(ratelimit(key=get_ratelimit_key, rate=get_ratelimit_rate, method='POST', block=True))
    def post(self, request, path):
        return self.operations(request, path)

    @method_decorator(ratelimit(key=get_ratelimit_key, rate=get_ratelimit_rate, method='PUT', block=True))
    def put(self, request, path):
        return self.operations(request, path)

    @method_decorator(ratelimit(key=get_ratelimit_key, rate=get_ratelimit_rate, method='PATCH', block=True))
    def patch(self, request, path):
        return self.operations(request, path)

    @method_decorator(ratelimit(key=get_ratelimit_key, rate=get_ratelimit_rate, method='DELETE', block=True))
    def delete(self, request, path):
        return self.operations(request, path)