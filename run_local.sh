#!/usr/bin/bash
set -e

# temp fix: update object acls
# issue: issue: https://github.com/localstack/localstack/issues/2407
aws --endpoint-url http://localhost:4566 s3api list-objects --bucket lautasofta-local-media --query "(Contents)[].[Key]" --output text | while read line ; do aws --endpoint-url http://localhost:4566 s3api put-object-acl --acl public-read --bucket lautasofta-local-media --key $line ; done

# app
sam build
sam local start-api --env-vars local_env.json --port 3002 --docker-network host
