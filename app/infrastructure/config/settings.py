from functools import lru_cache

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseModel):
    title: str
    debug: bool
    prefix: str
    description: str
    version: str
    openapi_tags: list[dict[str, str]]


class DatabaseSettings(BaseModel):
    url: str
    echo: bool


class JwtSettings(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    environment: str = Field(
        default='development', validation_alias='APP_ENV'
    )
    app_title: str = Field(
        default='FastAPI Education', validation_alias='APP_TITLE'
    )
    app_debug: bool = Field(
        default=True, validation_alias='APP_DEBUG'
    )
    api_prefix: str = Field(
        default='/api', validation_alias='API_PREFIX'
    )
    database_url: str = Field(
        default='sqlite+aiosqlite:///./fastapi_education.db',
        validation_alias='DATABASE_URL',
    )
    database_echo: bool = Field(
        default=False, validation_alias='DATABASE_ECHO'
    )
    jwt_secret_key: str = Field(validation_alias='JWT_SECRET_KEY')
    jwt_algorithm: str = Field(
        default='HS256', validation_alias='JWT_ALGORITHM'
    )
    jwt_access_token_expire_minutes: int = Field(
        default=30,
        validation_alias='JWT_ACCESS_TOKEN_EXPIRE_MINUTES',
    )
    jwt_refresh_token_expire_days: int = Field(
        default=7,
        validation_alias='JWT_REFRESH_TOKEN_EXPIRE_DAYS',
    )

    app_version: str = "1.0.0"
    app_description: str = (
        "Online school API built with clean architecture. "
        "At the first stage, the application supports public content reading "
        "and administrative management of courses, "
        "modules, sections and lectures."
    )
    openapi_tags: list[dict[str, str]] = [
        {
            "name": "Content",
            "description": (
                "Public endpoints for reading courses, "
                "course structure and lectures."
            ),
        },
        {
            "name": "Admin",
            "description": (
                'Management endpoints for authors and administrators '
                'who create and modify learning content.'
            ),
        },
        {
            "name": "Auth",
            "description": (
                "Endpoints for user registration and login "
                "with JWT token issuing."
            ),
        },
        {
            'name': 'Learning',
            'description': (
                'Authenticated endpoints for question attempts, '
                'answer submission and learning results.'
            ),
        },
    ]

    @property
    def api(self) -> ApiSettings:
        return ApiSettings(
            title=self.app_title,
            debug=self.app_debug,
            prefix=self.api_prefix,
            description=self.app_description,
            version=self.app_version,
            openapi_tags=self.openapi_tags
        )

    @property
    def database(self) -> DatabaseSettings:
        return DatabaseSettings(
            url=self.database_url,
            echo=self.database_echo,
        )

    @property
    def jwt(self) -> JwtSettings:
        return JwtSettings(
            secret_key=self.jwt_secret_key,
            algorithm=self.jwt_algorithm,
            access_token_expire_minutes=self.jwt_access_token_expire_minutes,
            refresh_token_expire_days=self.jwt_refresh_token_expire_days
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
