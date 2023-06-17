FROM python:3.10-alpine AS base

RUN apk add git
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install