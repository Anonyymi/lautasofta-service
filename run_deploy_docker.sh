#!/bin/bash

# build & deploy
DB_PASSWORD="root" docker-compose -p lautasofta_service -f ./deployment/docker/docker-compose.yaml up --build -d
