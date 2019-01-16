"""Flask Logger Extension module."""
import logging
import sys

try:
    from sentry_sdk import init as sentry_init
    from sentry_sdk.hub import GLOBAL_HUB
    from sentry_sdk.integrations.logging import LoggingIntegration
    from sentry_sdk.integrations.flask import FlaskIntegration
    SENTRY_IMPORTED = True
except ImportError:
    SENTRY_IMPORTED = False

LOGGERS = {}


class Logger():
    """Class to wrap the Flask app to provide awesome logging."""

    def __init__(self, app=None, config=None):
        self.config = config
        if app is not None:
            self.app = app
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app, config=None):
        """Init Flask Extension."""
        if config is not None:
            self.config = config
        elif self.config is None:
            self.config = app.config

        self.config.setdefault('LOG_LEVEL', logging.ERROR)

    def _log(self, name, dsn):
        """Get a logger with given name setup for environment."""
        logger = LOGGERS.get((name, dsn))

        if not logger:
            logger = logging.getLogger(name)
            logger.handlers = []

            self._setup_stdout(logger)

            sentry_dsn = dsn or self.config.get('SENTRY_DSN')
            if sentry_dsn:
                self._setup_sentry(logger, sentry_dsn)

            LOGGERS[(name, dsn)] = logger

        return logger

    def _setup_sentry(self, logger, dsn):
        if not SENTRY_IMPORTED:
            raise Exception('If specifying SENTRY_DSN, sentry_sdk must be installed'
                            ' (pip install flask-logger[Sentry])')

        env = self.config.get('environment') or self.config.get('env')
        sentry_init(dsn=dsn, integrations=[FlaskIntegration()], environment=env)
        sentry_integration = GLOBAL_HUB.get_integration(LoggingIntegration)
        logger.addHandler(sentry_integration._handler)  # pylint: disable=protected-access

    def _setup_stdout(self, logger):
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(self.config['LOG_LEVEL'])

        # Better format for console scanning
        fmt = (self.config.get('LOG_FORMAT_CONSOLE') or
               '%(asctime)s %(name)10s %(levelname)10s: %(message)10s')
        fmt_date = self.config.get('LOG_FORMAT_TIME') or '%Y-%m-%dT%T'
        formatter = logging.Formatter(fmt, fmt_date)

        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)

    def debug(self, name, message, extra=None, dsn=None):
        """Log debug level message to named logger."""
        self._log(name, dsn).debug(message, extra=extra)

    def info(self, name, message, extra=None, dsn=None):
        """Log info level message to named logger."""
        self._log(name, dsn).info(message, extra=extra)

    def warning(self, name, message, extra=None, dsn=None):
        """Log warning level message to named logger."""
        self._log(name, dsn).warning(message, extra=extra)

    def error(self, name, message, extra=None, dsn=None):
        """Log error level message to named logger."""
        self._log(name, dsn).error(message, extra=extra)

    def critical(self, name, message, extra=None, dsn=None):
        """Log critical level message to named logger."""
        self._log(name, dsn).critical(message, extra=extra)

    def exception(self, name, message, extra=None, dsn=None):
        """Log exception level message to named logger."""
        self._log(name, dsn).exception(message, extra=extra)
