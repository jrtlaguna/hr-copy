# mugna-hr

This repository is used for the backend of an hr application developed with Django.

## [Dockerized Development Environment](/README-docker.md)

## Local Environment Setup

### Features

1. **Rest API** login using [django rest framework]

### Requirements

1. Python 3.8
2. Pipenv
3. PostgreSQL

### Installation

1. Install `pipenv`
2. Clone this repo and `cd hrapp`
3. Run `pipenv --python 3.8`
4. Run `pipenv install`
5. Run `cp .env.example .env`
6. Update .env file

## Setup postgres db and mugna_hr user

```bash
sudo -u postgres psql

CREATE DATABASE mugna_hr;

CREATE USER mugna_hr WITH PASSWORD 'mugna_hr';
ALTER ROLE mugna_hr SET client_encoding TO 'utf8';
ALTER ROLE mugna_hr SET default_transaction_isolation TO 'read committed';
ALTER ROLE mugna_hr SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE mugna_hr TO mugna_hr;
```

## Configure .env File

1. Copy `.env.example` to `.env` and customize.

2. Set `DATABASE_URL` to `POSTGRES_URL=postgres://mugna_hr:mugna_hr@localhost:5432/mugna_hr`.

### Getting Started

1. Run `pipenv shell`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Create superuser `python manage.py createsuperuser`
5. Run `python manage.py runserver`
