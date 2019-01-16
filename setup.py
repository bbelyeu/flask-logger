"""Additional logging for Flask apps."""
from setuptools import setup

setup(
    name='Flask-Logger',
    version='1.0.3',
    url='https://github.com/bbelyeu/flask-logger',
    download_url='https://github.com/bbelyeu/flask-logger/archive/1.0.2.zip',
    license='MIT',
    author='Brad Belyeu',
    author_email='bradleylamar@gmail.com',
    description='Convenience logger for Flask apps',
    long_description=__doc__,
    packages=['flask_logger'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    extras_require={
        'Sentry': ['sentry-sdk']
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords=['flask', 'logging', 'logger', 'api'],
    test_suite='flask_logger.tests',
)
