from setuptools import setup, find_packages


README = open('README.rst').read()
VERSION = __import__("pydiscourse").__version__


setup(
    name="pydiscourse",
    version=VERSION,
    description="A Python library for the Discourse API",
    long_description=README,
    author="Marc Sibson and contributors",
    author_email="ben+pydiscourse@benlopatin.com",
    license="BSD",
    url="https://github.com/bennylope/pydiscourse",
    packages=find_packages(exclude=["tests.*", "tests"]),
    install_requires=['requests>=2.0.0'],
    tests_require=['mock'],
    test_suite='tests',
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
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    zip_safe=False,
)
