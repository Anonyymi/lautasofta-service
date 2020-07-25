#!/usr/bin/bash
set -e

# init local docker services
docker-compose -f local_env.yaml up -d

# init database clean+migrate
flyway -configFiles=./database/flyway.conf clean
flyway -configFiles=./database/flyway.conf migrate

# build app
sam build
aws --endpoint-url http://localhost:4566 cloudformation deploy \
    --template-file "./.aws-sam/build/template.yaml" \
    --stack-name "lautasofta-service"
