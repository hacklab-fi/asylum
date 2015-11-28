#!/bin/sh

# You should have: git remote add repo source
# usage: docker/test_pull_request.sh repo issue-

git checkout upstream/master
git pull $1 $2
docker build -t asylum_test .
echo "Starting test server."
echo "To gain shell, run: docker exec -it asylum_test bash"
docker run --rm --name asylum_test -it -p 8000:8000 -p 1080:1080 asylum_test
