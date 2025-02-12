from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import RegisterSerializer

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
class UserAccountAPIView(APIView):
    def get(self, request):
        user_id = request.headers['id']

        print(user_id)
        
        return Response({'user' : user_id}, status=status.HTTP_200_OK)