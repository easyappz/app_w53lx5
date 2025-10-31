from dataclasses import dataclass
from typing import Optional, Tuple

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .jwt_utils import verify_token


@dataclass
class SimpleUser:
    username: str
    is_authenticated: bool = True


class JWTAuthentication(BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request) -> Optional[Tuple[SimpleUser, str]]:
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

        user = SimpleUser(username=username)
        return user, token
