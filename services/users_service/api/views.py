from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import RegisterSerializer, UserSerializer

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
class UserAccountAPIView(APIView):    
    def get(self, request):
        user_id = request.headers.get("id")
        if not user_id:
            return Response({"error": "User ID is required"}, status=400)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=400)
        
        user_serializer = UserSerializer(user).data
        
        return Response({'user' : user_serializer}, status=status.HTTP_200_OK)