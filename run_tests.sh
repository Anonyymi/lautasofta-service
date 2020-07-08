#!/usr/bin/bash
set -e

# db
flyway -configFiles=./database/flyway.conf clean
flyway -configFiles=./database/flyway.conf migrate

# app
python -m pytest service/tests/ -v
