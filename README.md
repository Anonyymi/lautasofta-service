# lautasofta-service

[![Build Status](https://travis-ci.org/Anonyymi/lautasofta-service.svg?branch=master)](https://travis-ci.org/Anonyymi/lautasofta-service)

## Development

Local environment is setup so that localstack is used to simulate the aws cloud.

Install+configure aws cli, aws sam cli, docker, localstack & flyway-cli to get started.

## Deployment

### Docker

The service has docker-compose config to deploy it to local or remote machine.

#### Deploy to local machine example
```bash
DB_PASSWORD="your_db_pass" docker-compose -p lautasofta_service -f ./deployment/docker/docker-compose.yaml up -d
```

#### Deploy to remote machine example
```bash
DOCKER_HOST="ssh://server@remote.addr" DB_PASSWORD="your_db_pass" docker-compose -p lautasofta_service -f ./deployment/docker/docker-compose.yaml up -d
```

### AWS

For cost saving purposes, the service is intended to be deployed outside a VPC.
This means, that the database must be facing public internet, which is not ideal security-wise.
Firewall (for example, SecurityGroups) should be used to secure the database.
Furthermore, the connection between the service and the database should be encrypted.

## TODO

* Implement JWT-based authentication & authorization
  * Currently request admin status is decided from ipv4_addr
* Implement alternative uploaded files storage system
  * Currently the only implemented provider is aws s3
* Implement basic post related operations
  * Post refer_to id list
  * Post refer_from id list
  * Edit post (same restriction logic as with delete post)
