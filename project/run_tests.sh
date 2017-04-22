#!/usr/bin/env bash
sudo pip install -r requirements/test.txt
sudo -u postgres service postgresql start
export PGPASSWORD=asylum; while true; do psql -q asylum -c 'SELECT 1;' 1>/dev/null 2>&1 ; if [ "$?" -ne "0" ]; then echo "Waiting for psql"; sleep 1; else break; fi; done
sudo -u postgres psql -U postgres -d postgres -c "alter user asylum createdb;"

py.test -v $*
