import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
        print(f"full_url : {full_url}")
        params = request.query_params
        if params:
            full_url += f"?{params.urlencode()}"
        method = request.method.lower()
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
        
    def get(self, request, path):
        return self.operations(request, path)

    def post(self, request, path):
        return self.operations(request, path)

    def put(self, request, path):
        return self.operations(request, path)

    def patch(self, request, path):
        return self.operations(request, path)

    def delete(self, request, path):
        return self.operations(request, path)