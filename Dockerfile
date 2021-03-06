FROM python:3.8

WORKDIR /mugna

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y curl unzip libgtk-3-0 postgresql-client \
    && apt-get clean all \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install psycopg2-binary

RUN pip install pipenv \ 
    && pipenv install --deploy --system

ARG SECRET_KEY
ARG HOST
ARG DATABASE_URL
RUN python manage.py collectstatic --no-input

RUN adduser --disabled-password --gecos "" mugna_hr
USER mugna_hr

EXPOSE 8000