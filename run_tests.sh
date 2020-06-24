#!/usr/bin/bash
set -e

# db
docker-compose -f local_env.yaml up -d
flyway -configFiles=./database/flyway.conf clean
flyway -configFiles=./database/flyway.conf migrate

# app
python -m pytest service/tests/ -v
