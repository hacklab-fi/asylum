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
set +e
export PGPASSWORD=asylum; while true; do psql -q asylum -c 'SELECT 1;' 1>/dev/null 2>&1 ; if [ "$?" -ne "0" ]; then echo "Waiting for psql"; sleep 1; else break; fi; done
set -e

# Start forego or execute a command in the virtualenv
if [ "$#" -eq 0 ]; then
  echo "Starting devel server"
  maildump --http-ip 0.0.0.0 -p ~/maildump.pid &
  npm run build
  npm run watch &
  NPM=$!
  ./manage.py runserver 0.0.0.0:8000
  maildump -p ~/maildump.pid --stop
else
  echo "Calling $@"
  "$@"
fi
