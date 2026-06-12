from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from jwt.exceptions import InvalidTokenError as JwtInvalidTokenError

from app.application.interfaces.services.token_service import TokenService
from app.infrastructure.config import get_settings


class InvalidTokenError(Exception):
    pass


class JwtTokenService(TokenService):
    def __init__(self) -> None:
        settings = get_settings()
        self.secret_key = settings.jwt.secret_key
        self.algorithm = settings.jwt.algorithm
        self.access_token_expire_minutes = (
            settings.jwt.access_token_expire_minutes
        )
        self.refresh_token_expire_days = settings.jwt.refresh_token_expire_days

    def create_access_token(self, user_id: UUID, role: str) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=self.access_token_expire_minutes,
        )
        payload = {
            'sub': str(user_id),
            'role': role,
            "token_type": "access",
            'exp': expires_at,
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: UUID, role: str) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=self.refresh_token_expire_days,
        )
        payload = {
            'sub': str(user_id),
            'role': role,
            "token_type": "refresh",
            'exp': expires_at,
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_refresh_token(self, token: str) -> UUID:
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
        except JwtInvalidTokenError as exc:
            raise InvalidTokenError('Token is invalid or expired.') from exc

        if payload.get('token_type') != 'refresh':
            raise InvalidTokenError('Not a refresh token.')

        subject = payload.get('sub')
        if subject is None:
            raise InvalidTokenError('Token does not contain subject.')

        return UUID(subject)

    def get_user_id(self, token: str) -> UUID:
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
        except JwtInvalidTokenError as exc:
            raise InvalidTokenError('Token is invalid or expired.') from exc

        if payload.get('token_type') != 'access':
            raise InvalidTokenError('Not an access token.')

        subject = payload.get('sub')
        if subject is None:
            raise InvalidTokenError('Token does not contain subject.')

        return UUID(subject)
