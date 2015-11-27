#! /bin/bash

set -e

VENV_DIR_PATH=/opt/asylum/venv/

# activate virtualenv
. $VENV_DIR_PATH/bin/activate

# make sure postgresql is running
service postgresql start

# Start forego or execute a command in the virtualenv
if [ "$#" -eq 0 ]; then
  ./manage.py runserver 0.0.0.0:8000
else
  "$@"
fi
