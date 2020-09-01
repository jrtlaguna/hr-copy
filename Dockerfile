FROM python:3.8

WORKDIR /mugna

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y curl unzip git libgtk-3-0 locales postgresql-client \
    && apt-get clean all \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i -e 's/# en_CA.UTF-8 UTF-8/en_CA.UTF-8 UTF-8/' /etc/locale.gen \
    && echo 'LANG="en_CA.UTF-8"\nLC_ALL="en_CA.UTF-8"\nLC_CTYPE="en_CA.UTF-8"' > /etc/default/locale \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && update-locale

COPY . .

RUN pip install psycopg2-binary

RUN pip3 install --no-cache-dir -q 'pipenv==2018.11.26' \ 
    && pipenv install --deploy --system

ARG SECRET_KEY
ARG HOST
ARG DATABASE_URL
RUN python manage.py collectstatic --no-input

RUN adduser --disabled-password --gecos "" mugna_hr
USER mugna_hr

EXPOSE 8000