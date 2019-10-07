#!/usr/bin/env bash

pip install -r requirements.txt

export FLASK_APP="blockclient.py"

flask db upgrade

mkdir ./uploads
