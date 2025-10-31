from typing import Optional, Tuple

from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .jwt_utils import verify_token


class JWTAuthentication(BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request) -> Optional[Tuple[object, str]]:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            raise AuthenticationFailed("Invalid Authorization header format. Use 'Bearer <token>'.")

        token = parts[1]
        try:
            payload = verify_token(token)
        except ValueError as exc:
            raise AuthenticationFailed(str(exc)) from exc

        username = payload.get("sub")
        if not username:
            raise AuthenticationFailed("Invalid token payload.")

        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as exc:
            raise AuthenticationFailed("User not found") from exc

        return user, token
