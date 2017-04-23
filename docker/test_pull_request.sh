#!/bin/bash
# Make sure the id is here
if [ "$1" == "" ]
then
    echo "Usage:\n  test_pull_request.sh ID\n"
    exit 1
fi
ID=$1
CURRENT_BRANCH=`git rev-parse --abbrev-ref HEAD`

# "realpath" utility is not installed by default on all Linuxen and we need the true path
SCRIPTDIR=$(python2.7 -c 'import os,sys;print os.path.dirname(os.path.realpath(sys.argv[1]))' "$0")

# Make sure we're in the correct place to run git commands no matter where we were called from
cd `dirname "$SCRIPTDIR"`

# Make sure we have upstream
git remote | grep -q upstream
if [ "$?" == "1" ]
then
    git remote add upstream https://github.com/hacklab-fi/asylum.git
fi

git fetch upstream master

# Local branch exists, remove it
git rev-parse --verify test-$ID
if [ "$?" == "0" ]
then
    git branch -D test-$ID
fi

git fetch upstream pull/$ID/head:test-$ID
if [ "$?" != "0" ]
then
    exit 1
fi

# Store current branch
BRANCH=`git rev-parse --abbrev-ref HEAD`

set -e
git checkout test-$ID
git rebase upstream/master

# Run tests
$SCRIPTDIR/run_unit_tests.sh

git checkout $BRANCH
git branch -D test-$ID
echo "Temporary branch test-$ID was removed, to check it out again run: git fetch upstream pull/$ID/head:test-$ID"
