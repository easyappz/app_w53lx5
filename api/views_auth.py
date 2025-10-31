from django.contrib.auth import authenticate, get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    MeSerializer,
    ErrorSerializer,
)
from .jwt_utils import issue_token


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses={
            201: LoginSerializer,  # same shape: {username, token}
            400: ErrorSerializer,
        },
        tags=["auth"],
        summary="Register a new user",
        description=(
            "Registers a user in database (SQLite). Returns a JWT token in response body."
        ),
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data["username"].strip()
        password = serializer.validated_data["password"]

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            return Response({"detail": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(username=username, password=password)
        token = issue_token(username)
        return Response({"username": username, "token": token}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: LoginSerializer,  # {username, token}
            400: ErrorSerializer,
        },
        tags=["auth"],
        summary="Login user",
        description=(
            "Validates credentials against database and returns a JWT token in response body."
        ),
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data["username"].strip()
        password = serializer.validated_data["password"]

        user = authenticate(username=username, password=password)
        if user is None:
            # Fallback check in case auth backend isn't configured (shouldn't be necessary)
            User = get_user_model()
            try:
                user_obj = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
            if not user_obj.check_password(password):
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        token = issue_token(username)
        return Response({"username": username, "token": token}, status=status.HTTP_200_OK)


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={
            200: MeSerializer,
            401: ErrorSerializer,
        },
        tags=["auth"],
        summary="Get current user",
        description="Returns the username of the authenticated user.",
    )
    def get(self, request):
        return Response({"username": getattr(request.user, "username", "")}, status=status.HTTP_200_OK)
