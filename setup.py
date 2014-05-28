import codecs
import os

from setuptools import setup, find_packages


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname), 'rt').read()


# Provided as an attribute, so you can append to these instead
# of replicating them:
standard_exclude = ["*.py", "*.pyc", "*$py.class", "*~", ".*", "*.bak"]
standard_exclude_directories = [
    ".*", "CVS", "_darcs", "./build", "./dist", "EGG-INFO", "*.egg-info"
]


NAME = "pydiscourse"
DESCRIPTION = "A Python library for the Discourse API"
AUTHOR = "Marc Sibson"
AUTHOR_EMAIL = "sibson@gmail.com"
URL = "https://github.com/tindie/pydiscourse"
PACKAGE = "pydiscourse"
VERSION = __import__(PACKAGE).__version__


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.md"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=find_packages(exclude=["tests.*", "tests"]),
    entry_points={
        'console_scripts': [
            'pydiscoursecli = pydiscourse.main:main'
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    zip_safe=False,
)
