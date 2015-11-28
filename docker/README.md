# Building locally

    docker build -t hacklabfi/asylum .

# Running asylum

All of the docker commands are to be run at git repository root.

## Web server

The general idea is that a web server is going to appear at 8000 when you do docker run.

- On Linux: http://127.0.0.1:8000
- On other systems: http://192.168.100:8000 (maybe, check your docker-machine ip default)

## Maildump

- On Linux: http://127.0.0.1:1080
- On other systems: http://192.168.100:1080 (maybe, check your docker-machine ip default)

## Spawn a test server

Webserver exposed at port 8000.

    docker run --rm -it -p 8000:8000 -p 1080:1080 hacklabfi/asylum

This also **removes the container** afterwards.

## Create a test build and explore with bash

    docker run -it hacklabfi/asylum bash

## Test a pull request

    git checkout upstream/master
    git pull user pull_request
    docker build -t asylum_test .
    docker run --rm --name asylum_test -it -p 8000:8000 -p 1080:1080 asylum_test
    docker exec -it asylum_test bash

## Development environment (with project-folder mounted)

    docker run -it -p 8000:8000 -p 1080:1080 -v `pwd -P`/project:/opt/asylum hacklabfi/asylum
    docker exec -it container_name bash # Run in another terminal window

If you change anything that affects the build (requirements) you'll have to rebuild (see building locally).

Remember that if anything changes inside the docker container it might go to your git push.
Stay sharp! =)

This doesn't remove the container after ctrl-c and it can be started again if needed.

## Run in background

    docker run -d -p 8000:8000 -p 1080:1080 hacklabfi/asylum
