#!/bin/bash

export PYTHONPATH=$PYTHONPATH:${PWD%/*/*}:${PWD%/*}
export DJANGO_SETTINGS_MODULE=etv.settings
make html SPHINXBUILD='/Users/alejo8591/Documents/etv/venv/bin/sphinx-build'
