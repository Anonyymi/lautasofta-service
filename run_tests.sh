#!/usr/bin/bash
set -e

# init database clean+migrate
flyway -configFiles=./database/flyway.conf clean
flyway -configFiles=./database/flyway.conf migrate

# run app tests
python -m pytest --cov-report term --cov-report html --cov=service/api --cov=service/common --cov=service/thumb service/test/ -v
