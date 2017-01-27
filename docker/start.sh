#!/bin/bash -e
SCRIPTDIR=$(python -c 'import os,sys;print os.path.dirname(os.path.realpath(sys.argv[1]))' "$0")

# Make sure we're in the correct place relative to Dockerfile no matter where we were called from
cd `dirname "$SCRIPTDIR"`

docker build -t asylum_test .
echo "Starting test server."
echo "To connect to shell in this instance run: docker exec -it asylum_test /bin/bash"
echo "Then in that shell run: source ../asylum-venv/bin/activate"
docker run --rm --name asylum_test -it -p 8000:8000 -p 1080:1080 asylum_test
