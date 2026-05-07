import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(app):
    log_dir = app.config.get("LOG_DIR", "logs")
    log_level = app.config.get("LOG_LEVEL", "INFO")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "app.log")

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=5
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    file_handler.setFormatter(formatter)

    file_handler.setLevel(logging.INFO)

    # 🔥 IMPORTANT FIX
    app.logger.handlers.clear()   # remove default handlers
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.propagate = False

    app.logger.info("Logger initialized successfully")