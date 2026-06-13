import logging

from fastapi import APIRouter, Depends, status

from app.application.use_cases.auth.refresh_token import (
    RefreshTokenUseCase, RefreshTokenCommand
)
from app.domain.entities.user import User
from app.application.use_cases.auth.login_user import (
    LoginUserCommand, LoginUserUseCase
)
from app.application.use_cases.auth.register_user import (
    RegisterUserCommand,
    RegisterUserUseCase,
)
from app.presentation.api.dependencies import (
    get_current_user,
    get_login_user_use_case,
    get_register_user_use_case,
    get_refresh_token_user_use_case
)
from app.presentation.api.schemas import (
    CurrentUserResponse,
    ErrorResponse,
    LoginRequest,
    RegisteredUserResponse,
    RegisterUserRequest,
    TokenResponse,
)
from app.presentation.api.schemas.auth import RefreshTokenRequest

router = APIRouter(prefix='/auth', tags=['Auth'])
logger = logging.getLogger('app.events')


@router.post(
    '/register',
    response_model=RegisteredUserResponse,
    status_code=status.HTTP_201_CREATED,
    description=(
        'Creates a new user account in the system. '
        'A public registration always creates a user with the student role.'
    ),
    responses={
        400: {
            'description': 'Domain or application validation error.',
            'model': ErrorResponse,
        },
    },
)
async def register_user(
        request: RegisterUserRequest,
        use_case: RegisterUserUseCase = Depends(get_register_user_use_case),
) -> RegisteredUserResponse:
    result = await use_case.execute(
        RegisterUserCommand(
            email=request.email,
            password=request.password,
        )
    )
    logger.info(
        'User registered',
        extra={'event': 'user_registered', 'email': request.email},
    )
    return RegisteredUserResponse.model_validate(result)


@router.post(
    '/login',
    response_model=TokenResponse,
    summary='Login user',
    description=(
        'Authenticates a user by email and password and returns a '
        'JWT access token.'
    ),
    responses={
        400: {
            'description': 'Invalid email or password.',
            'model': ErrorResponse,
        },
    },
)
async def login_user(
        request: LoginRequest,
        use_case: LoginUserUseCase = Depends(get_login_user_use_case),
) -> TokenResponse:
    result = await use_case.execute(
        LoginUserCommand(
            email=request.email,
            password=request.password,
        )
    )
    logger.info(
        'User logged in',
        extra={'event': 'user_login', 'email': request.email},
    )
    return TokenResponse(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        token_type=result.token_type,
    )


@router.post(
    '/refresh',
    response_model=TokenResponse,
    summary='Refresh token',
    description=(
        'Get new JWT access token.'
    ),
    responses={
        401: {
            'description': 'Refresh token is invalid or expired.',
            'model': ErrorResponse,
        },
    },
)
async def refresh_token(
    request: RefreshTokenRequest,
    use_case: RefreshTokenUseCase = Depends(get_refresh_token_user_use_case),
) -> TokenResponse:
    result = await use_case.execute(RefreshTokenCommand(request.refresh_token))
    return TokenResponse(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        token_type=result.token_type,
    )


@router.get(
    '/me',
    response_model=CurrentUserResponse,
    summary='Get current user',
    description='Returns the currently authenticated user '
                'resolved from Bearer token.',
    responses={
        401: {
            'description': 'Authentication credentials '
            'are missing or invalid.',
            'model': ErrorResponse,
        },
    },
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> CurrentUserResponse:
    return CurrentUserResponse.model_validate(current_user)
