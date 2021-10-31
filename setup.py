#!/usr/bin/env python
from os.path import abspath, dirname, join
from setuptools import setup, find_packages


source_directory = dirname(abspath(__file__))

setup(
    name="checkio_json_serializer",
    version="0.2.0",
    python_requires=">=3.5",
    description="JSON serilizer for more complex objects",
    author="CheckiO",
    author_email="a.lyabah@checkio.org",
    url="https://github.com/CheckiO/checkio-json-serializer",
    packages=find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
