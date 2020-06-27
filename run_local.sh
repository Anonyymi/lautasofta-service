#!/usr/bin/bash
set -e

# app
sam build --use-container
sam local start-api --env-vars local_env.json --port 3002 --docker-network host
