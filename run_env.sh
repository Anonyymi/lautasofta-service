#!/usr/bin/bash
set -e

# init local docker services
docker-compose -f ./deployment/local/local_env.yaml up -d

# init database clean+migrate
flyway -configFiles=./deployment/local/flyway.conf -connectRetries=60 clean
flyway -configFiles=./deployment/local/flyway.conf -connectRetries=60 migrate

# build app
sam build --use-container -t ./deployment/aws/template.yaml
aws --endpoint-url http://localhost:4566 cloudformation deploy \
    --template-file "./.aws-sam/build/template.yaml" \
    --stack-name "lautasofta-service"
