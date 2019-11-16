#!/bin/sh

set -ex
docker build -t durka/hospital .
docker-compose down
docker-compose up

