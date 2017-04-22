#!/bin/bash -e
SCRIPTDIR=$(python -c 'import os,sys;print os.path.dirname(os.path.realpath(sys.argv[1]))' "$0")

# Make sure we're in the correct place relative to Dockerfile no matter where we were called from
cd `dirname "$SCRIPTDIR"`

if [ "$( docker images asylum_dev:latest )" == "" ]
then
    docker build -t asylum_dev .
fi
echo "Starting devel server."
echo "To connect to shell in this instance run: docker exec -it asylum_dev /bin/bash"
echo "Then in that shell run: source ../asylum-venv/bin/activate"
if [ "$(docker ps -a -q -f name=asylum_dev)" == "" ]
then
  echo "First run"
	set -x
	docker run --name asylum_dev -i -p 8000:8000 -p 1080:1080 -v `pwd -P`/project:/opt/asylum asylum_dev
  set +x
else
  set -x
	docker start -i asylum_dev
  set +x
fi
