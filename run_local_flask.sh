#!/usr/bin/bash
set -e

# app
FLASK_APP=./service/api/app.py flask run --port 3002
