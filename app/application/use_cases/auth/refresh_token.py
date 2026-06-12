from dataclasses import dataclass

from app.application.exceptions import InvalidCredentialsError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.interfaces.services.token_service import TokenService
from app.application.dto.auth_token import AuthToken


@dataclass(slots=True)
class RefreshTokenCommand:
    refresh_token: str


class RefreshTokenUseCase:
    def __init__(self, uow: UnitOfWork, token_service: TokenService):
        self.uow = uow
        self.token_service = token_service

    async def execute(self, command: RefreshTokenCommand) -> AuthToken:
        user_id = self.token_service.verify_refresh_token(
            command.refresh_token
        )
        async with self.uow:
            user = await self.uow.users.get_by_id(user_id)
            if user is None:
                raise InvalidCredentialsError('Invalid token.')
            access_token = self.token_service.create_access_token(
                user_id=user.id,
                role=user.role.value,
            )
            refresh_token = self.token_service.create_refresh_token(
                user_id=user.id,
                role=user.role.value,
            )
            return AuthToken(
                access_token=access_token,
                refresh_token=refresh_token,
            )
