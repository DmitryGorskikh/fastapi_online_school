import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.application.exceptions import (
    ApplicationError,
    CourseNotFoundError,
    LectureNotFoundError,
    ModuleNotFoundError,
    SectionNotFoundError,
    QuestionNotFoundError,
    AnswerOptionNotFoundError,
    QuestionAttemptNotFoundError,
    PermissionDeniedError as ApplicationPermissionDeniedError,
)
from app.domain.exceptions import DomainError
from app.presentation.api.schemas import ErrorResponse
from app.presentation.exceptions import (
    AuthenticationError,
    PermissionDeniedError as PresentationPermissionDeniedError,
)

logger = logging.getLogger('app.errors')


def build_error_response(
    request: Request, error: str, message: str, status_code: int
) -> JSONResponse:
    logger.warning(
            '%s: %s',
            error, message,
            extra={'path': request.url.path, 'status_code': status_code},
        )
    payload = ErrorResponse(error=error, message=message)
    return JSONResponse(status_code=status_code, content=payload.model_dump())


def build_error_response_raw(
    error: str, message: str, status_code: int
) -> JSONResponse:
    payload = ErrorResponse(error=error, message=message)
    return JSONResponse(status_code=status_code, content=payload.model_dump())


async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.error(
        'Unhandled exception',
        exc_info=exc,
        extra={'path': request.url.path},
    )
    return build_error_response_raw(
        error='internal_error',
        message='Internal server error.',
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def domain_error_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    return build_error_response(
        request=request,
        error='domain_error',
        message=str(exc),
        status_code=status.HTTP_400_BAD_REQUEST,
    )


async def application_error_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    return build_error_response(
        request=request,
        error='application_error',
        message=str(exc),
        status_code=status.HTTP_400_BAD_REQUEST,
    )


async def course_not_found_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    return build_error_response(
        request=request,
        error="course_not_found",
        message=str(exc),
        status_code=status.HTTP_404_NOT_FOUND,
    )


async def module_not_found_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    return build_error_response(
        request=request,
        error="module_not_found",
        message=str(exc),
        status_code=status.HTTP_404_NOT_FOUND,
    )


async def section_not_found_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    return build_error_response(
        request=request,
        error="section_not_found",
        message=str(exc),
        status_code=status.HTTP_404_NOT_FOUND,
    )


async def lecture_not_found_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    return build_error_response(
        request=request,
        error="lecture_not_found",
        message=str(exc),
        status_code=status.HTTP_404_NOT_FOUND,
    )


async def authentication_error_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    return build_error_response(
        request=request,
        error='authentication_error',
        message=str(exc),
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


async def permission_denied_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    return build_error_response(
        request=request,
        error='permission_denied',
        message=str(exc),
        status_code=status.HTTP_403_FORBIDDEN,
    )


async def application_permission_denied_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return build_error_response(
        request=request,
        error="permission_denied",
        message=str(exc),
        status_code=status.HTTP_403_FORBIDDEN,
    )


async def presentation_permission_denied_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return build_error_response(
        request=request,
        error="permission_denied",
        message=str(exc),
        status_code=status.HTTP_403_FORBIDDEN,
    )


async def question_not_found_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    return build_error_response(
        request=request,
        error="question_not_found",
        message=str(exc),
        status_code=status.HTTP_404_NOT_FOUND,
    )


async def answer_option_not_found_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return build_error_response(
        request=request,
        error="answer_option_not_found",
        message=str(exc),
        status_code=status.HTTP_404_NOT_FOUND,
    )


async def question_attempt_not_found_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return build_error_response(
        request=request,
        error="question_attempt_not_found",
        message=str(exc),
        status_code=status.HTTP_404_NOT_FOUND,
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, domain_error_handler)

    app.add_exception_handler(
        AuthenticationError, authentication_error_handler
    )
    app.add_exception_handler(
        ApplicationPermissionDeniedError,
        application_permission_denied_handler,
    )
    app.add_exception_handler(
        PresentationPermissionDeniedError,
        presentation_permission_denied_handler,
    )

    app.add_exception_handler(ApplicationError, application_error_handler)
    app.add_exception_handler(CourseNotFoundError, course_not_found_handler)
    app.add_exception_handler(ModuleNotFoundError, module_not_found_handler)
    app.add_exception_handler(SectionNotFoundError, section_not_found_handler)
    app.add_exception_handler(LectureNotFoundError, lecture_not_found_handler)
    app.add_exception_handler(
        QuestionNotFoundError, question_not_found_handler
    )
    app.add_exception_handler(
        AnswerOptionNotFoundError, answer_option_not_found_handler
    )
    app.add_exception_handler(
        QuestionAttemptNotFoundError, question_attempt_not_found_handler
    )
    app.add_exception_handler(Exception, unhandled_exception_handler)
