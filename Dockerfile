FROM python:3.11.8-alpine3.19 as compiler
LABEL maintainer="romafaum"
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

ENV VIRTUAL_ENV=/py
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -Ur /tmp/requirements.txt && rm -rf /tmp

