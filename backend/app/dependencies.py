# common stuff for routes, mostly for checking if user is logged in
import uuid

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_user_id_from_token
from app.core.exceptions import UnauthorizedException
from app.models.user import User


def _extract_token(authorization: str | None) -> str | None:
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1]


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    # get the user from the token, raise error if it fails
    token = _extract_token(authorization)
    if token is None:
        raise UnauthorizedException("Missing or malformed Authorization header")

    user_id_str = get_user_id_from_token(token, expected_type="access")
    if user_id_str is None:
        raise UnauthorizedException("Invalid or expired access token")

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise UnauthorizedException("Invalid token subject")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise UnauthorizedException("User not found")

    return user


def get_current_user_optional(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User | None:
    # same as above but doesn't crash if they aren't logged in
    # good for public pages that change a bit if you're logged in
    token = _extract_token(authorization)
    if token is None:
        return None

    user_id_str = get_user_id_from_token(token, expected_type="access")
    if user_id_str is None:
        return None

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        return None

    return db.query(User).filter(User.id == user_id).first()