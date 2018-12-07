"""Test the logger extension module."""

# pylint: disable=protected-access,redefined-outer-name,unused-variable,invalid-name
import logging
import unittest
from unittest.mock import MagicMock, patch

from flask import Flask

from flask_logger import Logger  # isort:skip
from flask_logger import extension  # isort:skip

TEST_DSN = 'http://foo:bar@sentry.local/1?timeout=1'  # Got this from raven-python repo tests


def create_app():
    """Create a Flask app for context."""
    app = Flask(__name__)
    logger = Logger()
    logger.init_app(app)
    return app


class TestLogger(unittest.TestCase):
    """Test Logger class."""

    def setUp(self):
        """Set up tests."""
        self.app = create_app()

    def tearDown(self):
        """Tear down tests."""
        # reset any mock loggers at module level
        extension.LOGGERS = {}  # noqa

    def test_default_config(self):
        """Test the default configs."""
        logger = Logger(self.app)
        self.assertEqual(logging.ERROR, logger.config['LOG_LEVEL'])

    def test_custom_app_config(self):
        """Test custom configs set on app."""
        self.app.config['LOG_LEVEL'] = logging.DEBUG
        logger = Logger(self.app)
        self.assertEqual(logging.DEBUG, logger.config['LOG_LEVEL'])

    def test_custom_kwarg_config_init(self):
        """Test custom configs passed via kwargs."""
        config = {
            'LOG_LEVEL': logging.INFO
        }
        logger = Logger(self.app, config)
        self.assertEqual(logging.INFO, logger.config['LOG_LEVEL'])

    def test_custom_kwarg_config_init_app(self):
        """Test custom configs passed via kwargs."""
        config = {
            'LOG_LEVEL': logging.INFO
        }
        obj = Logger()
        obj.init_app(self.app, config)
        self.assertEqual(logging.INFO, obj.config['LOG_LEVEL'])

    def test_log(self):
        """Test reusing same logger to validate module caching."""
        logger = Logger(self.app)
        extension.LOGGERS[('test', None)] = MagicMock()
        self.assertIsInstance(logger._log('test', None), MagicMock)

    def test_log_no_logger(self):
        """Test creating new logger."""
        logger = Logger(self.app)
        self.assertIsInstance(logger._log('no_mock', None), logging.Logger)
        self.assertIsInstance(logger._log('no_mock', TEST_DSN), logging.Logger)

    @patch('flask_logger.extension.GLOBAL_HUB.get_integration')
    @patch('flask_logger.extension.sentry_init')
    def test_setup_sentry(self, mock_handler, mock_client):
        """Test setup sentry."""
        mock_handler.return_value = MagicMock()
        logger = Logger(self.app)
        mock_logger = MagicMock()
        mock_logger.addHandler = MagicMock()

        logger._setup_sentry(mock_logger, TEST_DSN)
        assert mock_client.called
        assert mock_handler.called
        mock_logger.addHandler.assert_called_once()

    @patch('logging.Formatter')
    @patch('logging.StreamHandler')
    def test_setup_stdout(self, mock_handler, mock_formatter):
        """Test setup stdout."""
        logger = Logger(self.app)
        mock_logger = MagicMock()
        extension.LOGGERS[('test', None)] = mock_logger

        mock_handler.return_value = MagicMock()
        mock_formatter.return_value = MagicMock()

        logger._setup_stdout(mock_logger)
        assert mock_handler.called
        assert mock_formatter.called
        mock_handler.return_value.setFormatter.assert_called_once()
        mock_logger.addHandler.assert_called_once()

    def test_debug(self):
        """Test debug level logging."""
        logger = Logger(self.app)  # default level is error
        mock_logger = MagicMock()
        extension.LOGGERS[('foo', None)] = mock_logger

        logger.debug('foo', 'bar', extra={'foo': 'bar'})
        mock_logger.assert_not_called()

        config = {
            'LOG_LEVEL': logging.DEBUG
        }
        logger2 = Logger(self.app, config)
        mock_logger2 = MagicMock()
        extension.LOGGERS[('foo2', None)] = mock_logger2

        mock_logger2.debug = MagicMock()
        logger2.debug('foo2', 'bar', extra={'foo': 'bar'})
        mock_logger2.debug.assert_called_with('bar', extra={'foo': 'bar'})

    def test_info(self):
        """Test info level logging."""
        logger = Logger(self.app)  # default level is error
        mock_logger = MagicMock()
        extension.LOGGERS[('foo', None)] = mock_logger

        logger.info('foo', 'bar', extra={'foo': 'bar'})
        mock_logger.assert_not_called()

        config = {
            'LOG_LEVEL': logging.INFO
        }
        logger2 = Logger(self.app, config)
        mock_logger2 = MagicMock()
        extension.LOGGERS[('foo2', None)] = mock_logger2
        mock_logger2.info = MagicMock()

        logger2.info('foo2', 'bar', extra={'foo': 'bar'})
        mock_logger2.info.assert_called_with('bar', extra={'foo': 'bar'})

    def test_warning(self):
        """Test warning level logging."""
        logger = Logger(self.app)  # default level is error
        mock_logger = MagicMock()
        extension.LOGGERS[('foo', None)] = mock_logger

        logger.warning('foo', 'bar', extra={'foo': 'bar'})
        mock_logger.assert_not_called()

        config = {
            'LOG_LEVEL': logging.WARNING
        }
        logger2 = Logger(self.app, config)
        mock_logger2 = MagicMock()
        extension.LOGGERS[('foo2', None)] = mock_logger2
        mock_logger2.warning = MagicMock()

        logger2.warning('foo2', 'bar', extra={'foo': 'bar'})
        mock_logger2.warning.assert_called_with('bar', extra={'foo': 'bar'})

    def test_error(self):
        """Test error level logging."""
        logger = Logger(self.app)  # default level is error
        mock_logger = MagicMock()
        extension.LOGGERS[('foo', None)] = mock_logger
        mock_logger.error = MagicMock()

        logger.error('foo', 'bar', extra={'foo': 'bar'})
        mock_logger.error.assert_called_once_with('bar', extra={'foo': 'bar'})

    def test_critical(self):
        """Test critical level logging."""
        logger = Logger(self.app)  # default level is error
        mock_logger = MagicMock()
        extension.LOGGERS[('foo', None)] = mock_logger
        mock_logger.critical = MagicMock()

        logger.critical('foo', 'bar', extra={'foo': 'bar'})
        mock_logger.critical.assert_called_once_with('bar', extra={'foo': 'bar'})

    def test_exception(self):
        """Test critical level logging."""
        logger = Logger(self.app)  # default level is error
        mock_logger = MagicMock()
        extension.LOGGERS[('foo', None)] = mock_logger
        mock_logger.exception = MagicMock()

        logger.exception('foo', 'bar', extra={'foo': 'bar'})
        mock_logger.exception.assert_called_once_with('bar', extra={'foo': 'bar'})
