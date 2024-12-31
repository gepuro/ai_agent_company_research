#!/bin/sh -eu

cd `dirname $0`
cd ..

docker compose -f dockerfiles/docker-compose-dev.yml down
