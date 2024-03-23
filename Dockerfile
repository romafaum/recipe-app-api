FROM python:3.11.8-alpine3.19 as compiler
LABEL maintainer="romafaum"
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

ENV VIRTUAL_ENV=/py
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements.txt /tmp/requirements.txt

RUN apk add --update --no-cache postgresql-client


RUN apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev

RUN pip install -Ur /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps


