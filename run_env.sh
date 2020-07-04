#!/usr/bin/bash
set -e

# db
docker-compose -f local_env.yaml up -d
flyway -configFiles=./database/flyway.conf clean
flyway -configFiles=./database/flyway.conf migrate

# app
sam build
aws --endpoint-url http://localhost:4566 cloudformation deploy \
    --template-file "./.aws-sam/build/template.yaml" \
    --stack-name "lautasofta-service"
