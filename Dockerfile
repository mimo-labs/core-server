FROM python:3.7 as build

LABEL maintainer="Lucio Delelis <ldelelis@est.frba.utn.edu.ar>"

COPY requirements.txt /
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

FROM python:3.7-slim

WORKDIR /usr/src/app
COPY --from=build /wheels /wheels
COPY --from=build /requirements.txt .

RUN pip install --no-cache /wheels/*

COPY . /usr/src/app
ENV PYTHONUNBUFFERED 1

EXPOSE 8000/tcp
