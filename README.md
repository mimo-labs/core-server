# Django Mock Server

Simple project to load and serve mock JSON responses, with status code, and verb discrimination.

## Initial data

This repository provides a fixture of common use HTTP Verbs and Headers to get started with simple mocks.
To load it run `python manage.py loaddata initial.json`

## How to setup:

### Using Docker-Compose:

The docker-compose.yml service file already provides the working environment for the mock server to work. Simply run `docker-compose up`, and access the application from `localhost:8000`, or adjust the port and domain as you see fit.

### Using Docker:

This repository provides a Dockerfile to build an image of the server. A `docker build .` should suffice.

### Standalone:

The requirements file provides all the system dependencies, plus gunicorn to run in production mode.
