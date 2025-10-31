import hashlib
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
from .state import create_user, get_user, user_exists
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
            "Registers a user in in-memory storage. Returns a JWT token in response body."
        ),
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data["username"].strip()
        password = serializer.validated_data["password"]

        if user_exists(username):
            return Response({"detail": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        try:
            create_user(username=username, password_hash=password_hash)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

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
            "Validates credentials against in-memory storage and returns a JWT token in response body."
        ),
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data["username"].strip()
        password = serializer.validated_data["password"]

        user = get_user(username)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if user.get("password_hash") != password_hash:
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
