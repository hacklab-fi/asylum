#!/bin/sh

docker build -t asylum_dev .
docker run --name asylum_dev -d -p 8000:8000 -p 1080:1080 -v `pwd -P`/project:/opt/asylum asylum_dev
read -p "Press enter to stop and remove the server" dummy
docker stop asylum_dev
docker rm asylum_dev

