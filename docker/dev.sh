#!/bin/bash

# Check that we can access docker
docker ps >/dev/null 2>&1
if [ "$?" != "0" ]
then
    echo "Can't access docker, maybe try 'sudo adduser `whoami` docker'"
    echo "You may need to logout and log in again for that to take effect"
    exit 1
fi

# "realpath" utility is not installed by default on all Linuxen and we need the true path
SCRIPTDIR=$(python2.7 -c 'import os,sys;print os.path.dirname(os.path.realpath(sys.argv[1]))' "$0")

# Make sure we're in the correct place relative to Dockerfile no matter where we were called from
cd `dirname "$SCRIPTDIR"`

# Check if image is already built
docker inspect --type=image asylum_dev >/dev/null 2>&1
if [ "$?" != "0" ]
then
    set -e
    docker build -t asylum_dev .
fi
set -e
echo "Starting devel server."
echo "To connect to shell in this instance run: docker exec -it asylum_dev /bin/bash"
echo "Then in that shell run: source ../asylum-venv/bin/activate"
if [ "$(docker ps -a -q -f name=asylum_dev)" == "" ]
then
  echo "First run"
	set -x
	docker run --name asylum_dev -it -p 8000:8000 -p 1080:1080 -v `pwd -P`/project:/opt/asylum asylum_dev
  set +x
else
  set -x
	docker start -i asylum_dev
  set +x
fi
