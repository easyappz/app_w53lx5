from datetime import datetime, timedelta, timezone
from typing import Dict

import jwt

# Constants (no .env usage as per instructions)
SECRET_KEY_JWT = "easyappz-avitelog-jwt-secret-please-change-in-prod"
ALGORITHM = "HS256"


def issue_token(username: str, exp_minutes: int = 1440) -> str:
    now = datetime.now(timezone.utc)
    payload: Dict = {
        "sub": username,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=exp_minutes)).timestamp()),
    }
    token = jwt.encode(payload, SECRET_KEY_JWT, algorithm=ALGORITHM)
    # PyJWT may return str directly for pyjwt>=2.x
    return token if isinstance(token, str) else token.decode("utf-8")


def verify_token(token: str) -> Dict:
    try:
        payload = jwt.decode(token, SECRET_KEY_JWT, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError as exc:
        raise ValueError("Token has expired") from exc
    except jwt.InvalidTokenError as exc:
        raise ValueError("Invalid token") from exc

    sub = payload.get("sub")
    if not isinstance(sub, str) or not sub:
        raise ValueError("Invalid token payload: subject missing")
    return payload
