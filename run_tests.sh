#!/bin/bash
set -e

# init database clean+migrate
flyway -configFiles=./deployment/local/flyway.conf -connectRetries=60 clean
flyway -configFiles=./deployment/local/flyway.conf -connectRetries=60 migrate

# run app tests
python -m pytest --cov-report term --cov-report html --cov=services/web/api --cov=services/web/common --cov=services/web/thumb services/web/test/ -v
