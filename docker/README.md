# Building hacklabfi/asylum locally

docker build -t hacklabfi/asylum -f docker/Dockerfile .

# Running asylum

## Runserver, expose at port 8000

docker run -it -p 8000:8000 hacklabfi/asylum

## Explore the fs in virtualenv

docker run -it -p 8000:8000 hacklabfi/asylum bash

# Run in background

docker run -d -p 8000:8000 hacklabfi/asylum
