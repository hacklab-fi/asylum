#!/bin/bash
source ../asylum-venv/bin/activate
./manage.py generate_all
./manage.py exporttokens tokens.sqlite
./manage.py import_ndafile ndaparser/testdata.nda
