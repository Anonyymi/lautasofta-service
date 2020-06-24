#!/usr/bin/bash
set -e

python -m pytest service/tests/ -v
