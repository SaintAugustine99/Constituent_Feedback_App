from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        
        if user:
            # Create or get existing token (Simple Auth)
            # You might need to add 'rest_framework.authtoken' to INSTALLED_APPS first
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "username": user.username, "ward": user.ward.name if user.ward else None})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
