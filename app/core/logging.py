import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

import structlog

from app.core.config import settings

LOG_DIR = Path(settings.LOG_DIR)
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"


def setup_logging() -> None:
    """
    Здесь настройка структурированного логирования для приложения. | Here is the configure of structured logging for the application.
    """

    log_level=logging.DEBUG if settings.DEBUG else logging.INFO
    timestamper = structlog.processors.TimeStamper(fmt="iso")

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        timestamper,
        structlog.processors.format_exc_info,
    ]

    if settings.DEBUG:
        renderer = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=[
            *shared_processors,
            renderer,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    handlers = [
        RotatingFileHandler(
            LOG_FILE,
            maxBytes= 10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        ),
        logging.StreamHandler(sys.stdout),
    ]
    
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        handlers=handlers,
        force=True    
    )
