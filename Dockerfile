# Pull base image
FROM python:3.7.2-slim

# Instal system dependencies
RUN apt-get update
RUN apt-get install git -y

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV LANG C.UTF-8

# Create dynamic directories
RUN mkdir /logs /uploads

# Set work directory
WORKDIR /code

# Install pipenv
RUN pip install --upgrade pip
RUN pip install pipenv

# Install project dependencies
COPY Pipfile Pipfile.lock ./
RUN pipenv install --dev --ignore-pipfile --system