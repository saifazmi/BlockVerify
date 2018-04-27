#!/usr/bin/env bash

pip install -r requirements.txt

export FLASK_APP="blockAPI.py"

flask db upgrade
