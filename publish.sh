#!/bin/sh
black checkio_json_serializer tests
rm -rf dist/*
python3 setup.py bdist_wheel sdist
twine upload dist/*
