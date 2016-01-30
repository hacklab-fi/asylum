#!/bin/bash
SCRIPTDIR=$(python -c 'import os,sys;print os.path.dirname(os.path.realpath(sys.argv[1]))' "$0")
# Make sure the id is here
if [ "$1" == "" ]
then
    echo "Usage:\n  test_pull_request.sh ID\n"
    exit 1
fi
ID=$1

# Make sure we're in the correct place to run git commands no matter where we were called from
cd `dirname "$SCRIPTDIR"`

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

# Call the generic start script
$SCRIPTDIR/start.sh
