#!/bin/bash
# Make sure the id is here
if [ "$1" == "" ]
then
    echo "Usage:\n  test_pull_request.sh ID\n"
    exit 1
fi
ID=$1

# Make sure we have upstream
git remote | grep -q upstream
if [ "$?" == "1" ]
then
    git remote add upstream https://github.com/hacklab-fi/asylum.git
fi

git fetch upstream master
git fetch upstream pull/$ID/head:test-$ID
if [ "$?" != "0" ]
then
    exit 1
fi
set -e
git checkout test-$ID
git rebase upstream/master

docker build -t asylum_test .
echo "Starting test server."
echo "To gain shell, run: docker exec -it asylum_test bash"
docker run --rm --name asylum_test -it -p 8000:8000 -p 1080:1080 asylum_test
