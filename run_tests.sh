#!/usr/bin/bash
set -e

# init database clean+migrate
flyway -configFiles=./database/flyway.conf clean
flyway -configFiles=./database/flyway.conf migrate

# run app tests
python -m pytest service/test/ -v
