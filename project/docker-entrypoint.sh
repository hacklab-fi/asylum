#! /bin/bash

set -e

if [ ! -f .env ]; then
  echo "DATABASE_URL=postgres://asylum:asylum@localhost/asylum" > .env
fi

VENV_DIR_PATH=/opt/asylum-venv/

# activate virtualenv
. $VENV_DIR_PATH/bin/activate

# make sure postgresql is running
sudo -u postgres service postgresql start

# Start forego or execute a command in the virtualenv
if [ "$#" -eq 0 ]; then
  maildump --http-ip 0.0.0.0 -p ~/maildump.pid &
  npm run build
  npm run watch &
  NPM=$!
  ./manage.py runserver 0.0.0.0:8000
  maildump -p ~/maildump.pid --stop
else
  "$@"
fi
