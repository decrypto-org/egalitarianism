FROM python:3-alpine

RUN apk --no-cache --update-cache add build-base wget freetype-dev libpng-dev openblas-dev
RUN pip3 install pipenv

RUN set -ex && mkdir /app
WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .

RUN set -ex && pipenv install --deploy

COPY . .

ENTRYPOINT ["/bin/sh"]
