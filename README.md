# Flask-Logger

## Requirements

This project requires Python 3 (tested with 3.3-3.6) and Flask 0.12

## Installation

To install it, simply run

    pip install flask-logger

## Usage

Import it and wrap app

    from flask import Flask
    from flask_logger import Logger

    app = Flask(__name__)
    logger = Logger(app)

## Development

This project was written and tested with Python 3. Our builds currently support Python 3.3 to 3.6.

On a mac you can use the following commands to get up and running.
``` bash
brew install python3
```
otherwise run
``` bash
brew upgrade python3
```
to make sure you have an up to date version.

This project uses [pipenv](https://docs.pipenv.org) for dependency management. Install pipenv
``` bash
pip3 install pipenv
```

setup the project env
``` base
pipenv install --three --dev
```

create a .env file using this sample
``` bash
export PYTHONPATH=`pwd`
```

now load virtualenv and any .env file
```bash
pipenv shell
```

### Running tests

``` bash
./linters.sh && coverage run --source=flask_exceptions/ setup.py test
```

### Before committing any code

We have a pre-commit hook each dev needs to setup.
You can symlink it to run before each commit by changing directory to the repo and running

``` bash
cd .git/hooks
ln -s ../../pre-commit pre-commit
```
