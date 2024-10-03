from django.shortcuts import render
from .serializers import RegisterSerializer, LoginSerializer, ValidationErrorSerializer, TokenResponseSerializer
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema_view, extend_schema



@extend_schema_view(
    post=extend_schema(
        summary="Sign up a new user",
        request=RegisterSerializer,
        responses={
            201: RegisterSerializer,
            400: ValidationErrorSerializer
        }
    )
)
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]



@extend_schema_view(
    post=extend_schema(
        summary="Login in a user",
        request=LoginSerializer,
        responses={
            200: TokenResponseSerializer,
            400: ValidationErrorSerializer
        }
    )
)
class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        login = request.data.get('login')
        password = request.data.get('password')
        print(login, password, 's')
        if not login or not password:
            return Response({'error': 'Login va parol kiritilishi kerak'}, status=status.HTTP_400_BAD_REQUEST)

        if '@' in login:
            obj = User.objects.get(email=login)
            user = authenticate(username=obj.username, password=password)
        elif str(login).startswith('998') or str(login).startswith('+998'):
            obj = User.objects.get(phone_number=login)
            user = authenticate(username=obj.username, password=password)
        else:
            user = authenticate(username=login, password=password)

        if user is not None:
            return Response({'message': 'Muvaffaqiyatli kirish', 'tokens': {'access_token': user.token()['access'], 'refresh_token': user.token()['refresh']}}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Noto‘g‘ri login yoki parol'}, status=status.HTTP_401_UNAUTHORIZED)



