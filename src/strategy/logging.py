import logging
from logging import getLogger, basicConfig, Logger, RootLogger

logging.captureWarnings(True)

log_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARN,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}
