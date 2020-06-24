#!/usr/bin/bash
set -e

# db
docker-compose -f local_env.yaml up -d
flyway -configFiles=./database/flyway.conf clean
flyway -configFiles=./database/flyway.conf migrate

# app
sam build --use-container
sam local start-api --env-vars local_env.json --docker-network host
