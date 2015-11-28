# Building hacklabfi/asylum locally

docker build -t hacklabfi/asylum .

# Running asylum

## Runserver, expose at port 8000

docker run -it -p 8000:8000 hacklabfi/asylum

## Explore the fs in virtualenv

docker run -it -p 8000:8000 hacklabfi/asylum bash

## Running development environment

docker run -it -p 8000:8000 -v `pwd -P`/project:/opt/asylum hacklabfi/asylum

If you change anything that affects the build (requirements) you'll have to rebuild (see building locally).

Remember that if anything changes inside the docker container it might go to your git push.
Stay sharp! =)

# Run in background

docker run -d -p 8000:8000 hacklabfi/asylum

