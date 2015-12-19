#!/usr/bin/env bash

docker build -t asylum_test .
docker run --rm --name asylum_test -it asylum_test ./run_tests.sh
