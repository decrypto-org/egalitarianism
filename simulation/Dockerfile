FROM python:3

RUN pip3 install pipenv

RUN set -ex && mkdir /app
WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .

RUN set -ex && pipenv install

RUN mkdir -p /root/.config/matplotlib
RUN echo "backend : Agg" > /root/.config/matplotlib/matplotlibrc

COPY . .

ENTRYPOINT ["/bin/sh"]
