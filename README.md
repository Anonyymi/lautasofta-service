# lautasofta-service

[![Build Status](https://travis-ci.org/Anonyymi/lautasofta-service.svg?branch=master)](https://travis-ci.org/Anonyymi/lautasofta-service)

## development

Local environment is setup so that docker is used to simulate the aws cloud.

Install+configure aws cli, aws sam cli, docker, localstack & flyway-cli to get started.

## deployment

For cost saving purposes, the service is intended to be deployed outside a VPC.
This means, that the database must be facing public internet, which is not ideal security-wise.
Firewall (for example, SecurityGroups) should be used to secure the database.
Furthermore, the connection between the service and the database should be encrypted.


## TODO

* Decide administration system base architecture
  * Currently request admin status is decided from ipv4_addr
* Implement basic administration related operations
  * IP-ban
  * List bans with times and reasons
* Implement basic post related operations
  * Post refer_to id list
  * Post refer_from id list
  * Edit post (same restriction logic as with delete post)
