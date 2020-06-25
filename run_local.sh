#!/usr/bin/bash
set -e

# db
docker-compose -f local_env.yaml up -d --force-recreate localstack
flyway -configFiles=./database/flyway.conf clean
flyway -configFiles=./database/flyway.conf migrate

# app
sam build --use-container
aws --endpoint-url http://localhost:4581 cloudformation deploy \
    --template-file "./.aws-sam//build/template.yaml" \
    --stack-name "lautasofta-service"
sam local start-api --env-vars local_env.json --docker-network host
