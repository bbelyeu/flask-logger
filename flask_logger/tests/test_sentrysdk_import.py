"""Test the logger extension module."""
# pylint: disable=protected-access,redefined-outer-name,unused-variable,invalid-name
import importlib
import sys
import unittest

import sentry_sdk
from flask import Flask

import flask_logger

TEST_DSN = 'http://foo:bar@sentry.local/1?timeout=1'


def create_app():
    """Create a Flask app for context."""
    app = Flask(__name__)
    return app


class TestSentrySdkImport(unittest.TestCase):
    """Test logger when sentrysdk isn't installed."""

    def setUp(self):
        """Set up tests."""
        # Force flask_logger to load without sentry_sdk in the environment
        sys.modules['sentry_sdk'] = None
        importlib.reload(flask_logger.extension)
        self.app = create_app()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        """Tear down tests."""
        self.ctx.pop()
        # reset any mock loggers at module level
        # pylint: disable=invalid-name
        LOGGERS = {}  # noqa
        sys.modules['sentry_sdk'] = sentry_sdk
        # Reload flask logger to restore sys.modules to correct state
        importlib.reload(flask_logger.extension)

    def test_log_without_sentrysdk(self):
        """Test establishing logger when sentry_sdk isn't installed."""
        logger = flask_logger.Logger()
        logger.init_app(self.app)
        with self.assertRaises(Exception) as context:
            logger.error('no_sentry_sdk_logger', 'this will raise an exception', dsn=TEST_DSN)
        self.assertEqual(
            str(context.exception),
            'If specifying SENTRY_DSN, sentry_sdk must be installed '
            '(pip install flask-logger[Sentry])'
        )
