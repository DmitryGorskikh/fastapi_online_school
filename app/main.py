import logging

from fastapi import FastAPI

from app.infrastructure.config import get_settings
from app.presentation.api.handlers import register_exception_handlers
from app.presentation.api.routes import router as api_router
from app.infrastructure.logging.config import setup_logging
from app.presentation.api.middleware import LoggingMiddleware


def create_app() -> FastAPI:
    settings = get_settings()

    setup_logging(settings.environment)
    logger = logging.getLogger('app.startup')
    logger.info('Application is starting up')

    app = FastAPI(
        title=settings.api.title,
        debug=settings.api.debug,
        description=settings.api.description,
        version=settings.api.version,
        openapi_tags=settings.api.openapi_tags
    )

    app.add_middleware(LoggingMiddleware)

    register_exception_handlers(app)
    app.include_router(api_router)

    return app


app = create_app()
