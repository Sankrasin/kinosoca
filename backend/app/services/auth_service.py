# logic for signing up and logging in
import uuid

from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_user_id_from_token,
)
from app.core.exceptions import ConflictException, UnauthorizedException
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, AccessTokenResponse


def register_user(db: Session, payload: RegisterRequest) -> User:
    # see if email is taken
    existing_email = db.query(User).filter(User.email == payload.email).first()
    if existing_email:
        raise ConflictException("An account with this email already exists")

    # see if username is taken
    existing_username = db.query(User).filter(User.username == payload.username).first()
    if existing_username:
        raise ConflictException("This username is already taken")

    # save new user
    user = User(
        email=payload.email,
        username=payload.username,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, payload: LoginRequest) -> TokenResponse:
    # check email and password match
    user = db.query(User).filter(User.email == payload.email).first()
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise UnauthorizedException("Invalid email or password")

    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )


def refresh_access_token(db: Session, refresh_token: str) -> AccessTokenResponse:
    # check if refresh token is valid and get new access token
    user_id_str = get_user_id_from_token(refresh_token, expected_type="refresh")
    if user_id_str is None:
        raise UnauthorizedException("Invalid or expired refresh token")

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise UnauthorizedException("Invalid token subject")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise UnauthorizedException("User not found")

    return AccessTokenResponse(access_token=create_access_token(str(user.id)))