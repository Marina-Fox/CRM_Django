FROM python:3.12-slim-bookworm

WORKDIR /project

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --upgrade pip "poetry==2.2.1" &&\
    poetry config virtualenvs.create false --local

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev --no-root

COPY . .
