# Flask-Logger

[![Build Status](https://travis-ci.org/bbelyeu/flask-logger.svg?branch=master)](https://travis-ci.org/bbelyeu/flask-logger)
[![Coverage Status](https://coveralls.io/repos/github/bbelyeu/flask-logger/badge.svg?branch=master)](https://coveralls.io/github/bbelyeu/flask-logger?branch=master)

## Requirements

This project requires Python 3.6 and Flask 0.12

## Installation

To install it without Sentry support, simply run

    pip install flask-logger

To install it with Sentry support, run

    pip install flask-logger[Sentry]

## Usage

Import it and wrap app

    from flask import Flask
    from flask_logger import Logger

    app = Flask(__name__)
    logger = Logger(app)

## Configuration values

You can set the default logging level on your app with the config value `LOG_LEVEL`.

If you use Sentry with your project, you can setup [Sentry](https://sentry.io) logging by adding
the `SENTRY_DSN` configuration value. Your DSN can be retrieved from your project in Sentry.

If you do use Sentry, you may also want to specify an `ENV` (dev, staging, qa, prod, etc) in your
app's config so that the correct environment information can be sent to Sentry.

You can modify the console output format with the configuration values `LOG_FORMAT_CONSOLE` and
`LOG_FORMAT_TIME`. See the Python 3
[logging Formatter docs](https://docs.python.org/3/library/logging.html#logging.Formatter)
for more info.

## Development

This project was written and tested with Python 3. Our builds currently only test Python 3.6.

On a mac you can use the following commands to get up and running.
``` bash
brew install python3
```
otherwise run
``` bash
brew upgrade python3
```
to make sure you have an up to date version.

This project uses [pip-tools](https://pypi.org/project/pip-tools/) for dependency management. Install pip-tools
``` bash
pip3 install pip-tools
```

setup the project env
``` base
python -m venv venv
pip install -r requirements.txt -r requirements-dev.txt
```

create a .env file using this sample
``` bash
export PYTHONPATH=`pwd`
```

now load virtualenv and any .env file
```bash
source venv/bin/activate
```

### Running tests

``` bash
./linters.sh && coverage run --source=flask_logger/ setup.py test
```

### Before committing any code

We have a pre-commit hook each dev needs to setup.
You can symlink it to run before each commit by changing directory to the repo and running

``` bash
cd .git/hooks
ln -s ../../pre-commit pre-commit
```
