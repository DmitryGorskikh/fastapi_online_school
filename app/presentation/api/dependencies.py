from collections.abc import AsyncIterator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.application.use_cases.auth.refresh_token import RefreshTokenUseCase
from app.domain.entities.user import User

from app.application.use_cases.auth.login_user import LoginUserUseCase
from app.application.use_cases.courses.get_course import GetCourseUseCase
from app.application.use_cases.courses.get_course_structure import (
    GetCourseStructureUseCase
)
from app.application.use_cases.courses.get_courses import GetCoursesUseCase
from app.application.use_cases.lectures.get_lecture import GetLectureUseCase

from app.application.use_cases.courses.create_course import CreateCourseUseCase
from app.application.use_cases.courses.update_course import UpdateCourseUseCase
from app.application.use_cases.courses.delete_course import DeleteCourseUseCase

from app.application.use_cases.modules.create_module import CreateModuleUseCase
from app.application.use_cases.modules.update_module import UpdateModuleUseCase
from app.application.use_cases.modules.delete_module import DeleteModuleUseCase

from app.application.use_cases.sections.create_section import (
    CreateSectionUseCase
)
from app.application.use_cases.sections.update_section import (
    UpdateSectionUseCase
)
from app.application.use_cases.sections.delete_section import (
    DeleteSectionUseCase
)

from app.application.use_cases.lectures.create_lecture import (
    CreateLectureUseCase
)
from app.application.use_cases.lectures.update_lecture import (
    UpdateLectureUseCase
)
from app.application.use_cases.lectures.delete_lecture import (
    DeleteLectureUseCase
)

from app.infrastructure.database import SessionFactory, SqlAlchemyUnitOfWork

from app.application.interfaces.services.token_service import TokenService
from app.application.interfaces.services.password_hasher import PasswordHasher
from app.application.use_cases.auth.register_user import RegisterUserUseCase
from app.infrastructure.security.jwt_token_service import (
    InvalidTokenError, JwtTokenService
)
from app.infrastructure.security.password_hasher import PwdlibPasswordHasher
from app.presentation.exceptions import (
    AuthenticationError, PermissionDeniedError
)

from app.application.use_cases.answer_options.create_answer_option import (
    CreateAnswerOptionUseCase,
)
from app.application.use_cases.answer_options.update_answer_option import (
    UpdateAnswerOptionUseCase,
)
from app.application.use_cases.answer_options.delete_answer_option import (
    DeleteAnswerOptionUseCase,
)
from app.application.use_cases.questions.create_question import (
    CreateQuestionUseCase
)
from app.application.use_cases.questions.update_question import (
    UpdateQuestionUseCase
)
from app.application.use_cases.questions.delete_question import (
    DeleteQuestionUseCase,
)

from app.application.use_cases.question_attempts.get_question_attempt_result import (  # noqa: E501
    GetQuestionAttemptResultUseCase,
)
from app.application.use_cases.question_attempts.start_question_attempt import (  # noqa: E501
    StartQuestionAttemptUseCase,
)
from app.application.use_cases.question_attempts.submit_question_answer import (  # noqa: E501
    SubmitQuestionAnswerUseCase,
)

http_bearer = HTTPBearer(auto_error=False)


async def get_uow() -> AsyncIterator[SqlAlchemyUnitOfWork]:
    async with SqlAlchemyUnitOfWork(session_factory=SessionFactory) as uow:
        yield uow


def get_get_courses_use_case(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> GetCoursesUseCase:
    """UseCase для получения списка курсов."""
    return GetCoursesUseCase(course_repository=uow.courses)


def get_get_course_use_case(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> GetCourseUseCase:
    """UseCase для получения курса по id."""
    return GetCourseUseCase(course_repository=uow.courses)


def get_get_course_structure_use_case(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> GetCourseStructureUseCase:
    """UseCase для получения полной структуры курса."""
    return GetCourseStructureUseCase(
        course_repository=uow.courses,
        module_repository=uow.modules,
        section_repository=uow.sections,
        lecture_repository=uow.lectures,
    )


def get_get_lecture_use_case(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> GetLectureUseCase:
    """UseCase для получения лекции по id."""
    return GetLectureUseCase(lecture_repository=uow.lectures)


def get_create_course_use_case() -> CreateCourseUseCase:
    """UseCase для создания курса."""
    return CreateCourseUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_update_course_use_case() -> UpdateCourseUseCase:
    """UseCase для обновления курса."""
    return UpdateCourseUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_remove_course_use_case() -> DeleteCourseUseCase:
    """UseCase для удаления курса."""
    return DeleteCourseUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_create_module_use_case() -> CreateModuleUseCase:
    """UseCase для создания модуля."""
    return CreateModuleUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_update_module_use_case() -> UpdateModuleUseCase:
    """UseCase для обновления модуля."""
    return UpdateModuleUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_remove_module_use_case() -> DeleteModuleUseCase:
    """UseCase для удаления модуля."""
    return DeleteModuleUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_create_section_use_case() -> CreateSectionUseCase:
    """UseCase для создания раздела(секции)."""
    return CreateSectionUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_update_section_use_case() -> UpdateSectionUseCase:
    """UseCase для обновления раздела(секции)."""
    return UpdateSectionUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_remove_section_use_case() -> DeleteSectionUseCase:
    """UseCase для удаления раздела(секции)."""
    return DeleteSectionUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_create_lecture_use_case() -> CreateLectureUseCase:
    """UseCase для создания лекции."""
    return CreateLectureUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_update_lecture_use_case() -> UpdateLectureUseCase:
    """UseCase для обновления лекции."""
    return UpdateLectureUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_remove_lecture_use_case() -> DeleteLectureUseCase:
    """UseCase для удаления лекции."""
    return DeleteLectureUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_password_hasher() -> PasswordHasher:
    """Сервис для хэширования пароля."""
    return PwdlibPasswordHasher()


def get_token_service() -> TokenService:
    """Сервис для генерации токена."""
    return JwtTokenService()


def get_register_user_use_case() -> RegisterUserUseCase:
    """UseCase для регистрации пользователя."""
    return RegisterUserUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory),
        password_hasher=get_password_hasher(),
    )


def get_login_user_use_case() -> LoginUserUseCase:
    """UseCase для авторизации пользователя."""
    return LoginUserUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory),
        password_hasher=get_password_hasher(),
        token_service=get_token_service(),
    )


def get_refresh_token_user_use_case() -> RefreshTokenUseCase:
    """UseCase для получения обновления токена."""
    return RefreshTokenUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory),
        token_service=get_token_service(),
    )


def get_create_question_use_case() -> CreateQuestionUseCase:
    """UseCase для создания вопроса."""
    return CreateQuestionUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_update_question_use_case() -> UpdateQuestionUseCase:
    """UseCase для обновления вопроса."""
    return UpdateQuestionUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_remove_question_use_case() -> DeleteQuestionUseCase:
    """UseCase для удаления вопроса."""
    return DeleteQuestionUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_create_answer_option_use_case() -> CreateAnswerOptionUseCase:
    """UseCase для создания варианта ответа на вопрос."""
    return CreateAnswerOptionUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_update_answer_option_use_case() -> UpdateAnswerOptionUseCase:
    """UseCase для обновления варианта ответа на вопрос."""
    return UpdateAnswerOptionUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_remove_answer_option_use_case() -> DeleteAnswerOptionUseCase:
    """UseCase для удаления варианта ответа на вопрос."""
    return DeleteAnswerOptionUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_start_question_attempt_use_case() -> StartQuestionAttemptUseCase:
    """
    UseCase для просмотра вопроса для студента.
        - если can_submit = true, можно показать обычную форму ответа
        - если can_submit = false и is_solved = true,
        можно показать вопрос как уже решенный
        - если есть selected_option_ids и last_result_status,
        можно отрисовать прошлый выбор студента и итог последней попытки
    """
    return StartQuestionAttemptUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_submit_question_answer_use_case() -> SubmitQuestionAnswerUseCase:
    """UseCase для отправки варианта ответа на вопрос."""
    return SubmitQuestionAnswerUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_get_question_attempt_result_use_case(
) -> GetQuestionAttemptResultUseCase:
    """UseCase для получения результата ответа на вопрос."""
    return GetQuestionAttemptResultUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(http_bearer),
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
    token_service: TokenService = Depends(get_token_service),
) -> User:
    """Функция для получения текущего пользователя."""
    if credentials is None:
        raise AuthenticationError(
            'Authentication credentials were not provided.'
        )

    if credentials.scheme.lower() != 'bearer':
        raise AuthenticationError('Authentication scheme must be Bearer.')

    try:
        user_id = token_service.get_user_id(credentials.credentials)
    except InvalidTokenError as exc:
        raise AuthenticationError(str(exc)) from exc

    user = await uow.users.get_by_id(user_id)
    if user is None:
        raise AuthenticationError('User from token was not found.')

    return user


async def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Функция для проверки админа."""
    if not current_user.can_manage_platform():
        raise PermissionDeniedError('Admin access is required.')
    return current_user


async def get_current_author_or_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Функция для проверки админа и автора."""
    if not current_user.can_manage_content():
        raise PermissionDeniedError('Author or admin access is required.')
    return current_user
