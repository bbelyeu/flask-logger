"""Test the logger extension module."""
# pylint: disable=protected-access,redefined-outer-name,unused-variable,invalid-name
import importlib
import sys
import unittest

import raven
from flask import Flask

import flask_logger

TEST_DSN = 'http://foo:bar@sentry.local/1?timeout=1'


def create_app():
    """Create a Flask app for context."""
    app = Flask(__name__)
    return app


class TestRavenImport(unittest.TestCase):
    """Test logger when raven isn't installed."""

    def setUp(self):
        """Set up tests."""
        # Force flask_logger to load without raven in the environment
        sys.modules['raven'] = None
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
        sys.modules['raven'] = raven
        # Reload flask logger to restore sys.modules to correct state
        importlib.reload(flask_logger.extension)

    def test_log_without_raven(self):
        """Test establishing logger when raven isn't installed."""
        logger = flask_logger.Logger()
        logger.init_app(self.app)
        with self.assertRaises(Exception) as context:
            logger.error('no_raven_logger', 'this will raise an exception', dsn=TEST_DSN)
        self.assertEqual(
            str(context.exception),
            'If specifying SENTRY_DSN, raven must be installed (pip install flask-logger[Sentry])'
        )
