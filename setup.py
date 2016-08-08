from setuptools import find_packages
from setuptools import setup

setup(
    name='raccoon_log',
    version='1.0.2',
    description="Configure log to follow a pattern for all projects.",
    author="Raccoon",
    author_email="ti@raccoon.ag",
    url="https://www.raccoon.ag",
    packages=find_packages(),
    install_requires=[
        'git+git://github.com/sabrinamagalhaes/raccoon_notifier/#egg=raccoon_notifier',
    ],
    )
