# <!-- omit in toc -->Instructions to set up Dockerized Dev Environment

- [PREREQUISITES](#prerequisites)
  - [Docker](#docker)
- [SETUP & LAUNCH THE FIRST TIME](#setup--launch-the-first-time)
  - [Configure .env File](#configure-env-file)
  - [Configure settings.py File](#configure-hr/settings.py-file)
  - [Build the Docker Image](#build-the-docker-image)
  - [Run the Server Cluster for the First Time](#run-the-server-cluster-for-the-first-time)
  - [Shutdown all Services](#shutdown-all-services)
  - [Restart the Services](#restart-the-services)

# PREREQUISITES

Any OS will work since we're using docker.

## Docker

Install [Docker](https://hub.docker.com/) for your operating system and make sure you are able to download docker images from their repository.

# SETUP & LAUNCH THE FIRST TIME

Clone this repo and type in `$ cd mugna-hr`

## Configure .env File

1. Copy `.env.example` to `.env` and customize.

2. Comment out `DATABASE_URL`, Docker will handle the database connection.

3. Set `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` to `mugna_hr`

4. Set `DB_HOST` to `postgres`

## Configure hr/settings.py File

1. Go to `hr/settings.py`

2. Go to the DATABASES dictionary and set `HOST` to `db`

## Build the Docker Image

```sh
$ docker-compose build app
```

This will take a while since Docker will need to download the BASE image and setup the container. Wait till Docker prints out this message

```sh
Successfully tagged mugna-hr_app:latest
```

## Run the Server Cluster for the First Time

```sh
$ docker-compose up
```

It normally takes a while for the first boot. Wait until you start to see a bunch of messages from the worker processes or see the Django server notice.

## Create a superuser

Open a second terminal window (while `docker-compose up` is running in the first one)

```sh
# Get into the shell on the Docker container for the app (app in compose file)
$ docker-compose exec app /bin/bash

# Create a superuser account in Django
$ python manage.py createsuperuser

# Leave the Docker container's shell
$ exit
```

## Shutdown all Services

Inside the second terminal window where you accessed the container's shell, type:

```sh
$ docker-compose down
```

Wait until all the services are down.

## Restart the Services

```sh
$ docker-compose up
```

Wait until you see the Django "Starting development server at http://0.0.0:8000/" message and then visit [http://localhost:8000/api/docs](http://localhost:8000/api/docs) to load the Mugna-HR API documentation.
