#!/bin/bash
# Check that we can access docker
docker ps >/dev/null 2>&1
if [ "$?" != "0" ]
then
    echo "Can't access docker, maybe try 'sudo adduser `whoami` docker'"
    echo "You may need to logout and log in again for that to take effect"
    exit 1
fi
set -e

# "realpath" utility is not installed by default on all Linuxen and we need the true path
SCRIPTDIR=$(python2.7 -c 'import os,sys;print os.path.dirname(os.path.realpath(sys.argv[1]))' "$0")

# Make sure we're in the correct place relative to Dockerfile no matter where we were called from
cd `dirname "$SCRIPTDIR"`

docker build -t asylum_test .
echo "Starting test server."
echo "To connect to shell in this instance run: docker exec -it asylum_test /bin/bash"
echo "Then in that shell run: source ../asylum-venv/bin/activate"
docker run --rm --name asylum_test -it -p 8000:8000 -p 1080:1080 asylum_test
