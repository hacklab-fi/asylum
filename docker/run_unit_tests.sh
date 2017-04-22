#!/bin/bash -e
SCRIPTDIR=$(python -c 'import os,sys;print os.path.dirname(os.path.realpath(sys.argv[1]))' "$0")

# Make sure we're in the correct place relative to Dockerfile no matter where we were called from
cd `dirname "$SCRIPTDIR"`

docker build -t asylum_test .
docker run --rm --name asylum_test -it asylum_test ./run_tests.sh
