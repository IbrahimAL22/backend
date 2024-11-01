# views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignUpSerializer, SignInSerializer

class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer

class SignInView(generics.GenericAPIView):
    serializer_class = SignInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                # Create a JWT token for the user
                refresh = RefreshToken.for_user(user)
                return Response({
                    "token": str(refresh.access_token),  # Correctly access the access token
                    "username": user.username,  # Send the username
                    "message": "Login successful"
                }, headers={"Content-Type": "application/json; charset=utf-8"}, status=status.HTTP_200_OK)

            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
