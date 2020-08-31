#!/bin/bash

# build app
sam build --use-container -t ./deployment/aws/template.yaml
