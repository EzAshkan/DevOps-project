import json
import logging
import sys
import traceback
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service_name": getattr(
                record,
                "service_name",
                "task-manager-backend",
            ),
            "log_level": record.levelname,
            "source": getattr(record, "source", "server"),
            "type": getattr(record, "log_type", "application"),
            "logger": record.name,
            "message": record.getMessage(),
        }

        optional_fields = (
            "correlation_id",
            "protocol",
            "method",
            "endpoint",
            "status",
            "duration_ms",
            "instance",
        )

        for field in optional_fields:
            value = getattr(record, field, None)
            if value is not None:
                log[field] = value

        if record.exc_info:
            exc_type, exc_value, exc_tb = record.exc_info

            log["type"] = "exception"
            log["payload"] = {
                "exception_data": {
                    "error_message": str(exc_value),
                    "class": (
                        f"{exc_type.__module__}.{exc_type.__name__}"
                        if exc_type
                        else None
                    ),
                    "stack_trace": "".join(
                        traceback.format_exception(
                            exc_type,
                            exc_value,
                            exc_tb,
                        )
                    ),
                }
            }

        return json.dumps(
            log,
            ensure_ascii=False,
            default=str,
        )


def configure_logging(log_level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)

    # Uvicorn's own access log is disabled in Docker CMD.
    # Keep uvicorn internal messages using our JSON formatter.
    for logger_name in (
        "uvicorn",
        "uvicorn.error",
    ):
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.propagate = True
