#!/usr/bin/env sh

sudo -u postgres psql -U postgres -d postgres -c "alter user asylum createdb;"

./manage.py test $*
