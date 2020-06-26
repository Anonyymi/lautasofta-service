#!/usr/bin/bash
set -e

# db
docker-compose -f local_env.yaml up -d --force-recreate localstack
flyway -configFiles=./database/flyway.conf clean
flyway -configFiles=./database/flyway.conf migrate

# app
aws --endpoint-url http://localhost:4581 cloudformation deploy \
    --template-file "./.aws-sam//build/template.yaml" \
    --stack-name "lautasofta-service"
FLASK_APP=./service/api/app.py flask run --port 3000
