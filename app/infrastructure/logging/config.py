import json
import logging
import sys
from logging.config import dictConfig


class JsonFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        log = {
            'time': self.formatTime(record, '%Y-%m-%dT%H:%M:%S'),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }
        for key in (
            'method', 'path', 'status_code', 'duration_ms', 'event', 'user_id',
            'email', 'actor_id', 'course_id', 'module_id', 'section_id',
            'lecture_id', 'question_id', 'answer_option_id', 'task_id'
        ):
            if hasattr(record, key):
                log[key] = getattr(record, key)

        if record.exc_info:
            log['exception'] = self.formatException(record.exc_info)
        return json.dumps(log, ensure_ascii=False)


def setup_logging(environment: str) -> None:
    is_production = environment == 'production'

    dictConfig({
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'text': {
                    'format': '%(asctime)s | %(levelname)-8s | %(name)s | '
                    '%(message)s',
                },
                'json': {
                    '()': 'app.infrastructure.logging.config.JsonFormatter',
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'json' if is_production else 'text',
                    'stream': sys.stdout,
                },
            },
            'loggers': {
                'app': {
                    'handlers': ['console'],
                    'level': 'INFO' if is_production else 'DEBUG',
                    'propagate': False,
                },
            },
            'root': {
                'handlers': ['console'],
                'level': 'INFO',
            },
        })
