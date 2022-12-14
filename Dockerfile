# FROM python:3.7-bullseye
FROM python:3.8.10-slim-buster

WORKDIR /app

COPY ./ /app

RUN apt-get update && apt-get clean
RUN apt-get install build-essential -y


# Install ffmpeg
RUN apt-get install --no-install-recommends -y ffmpeg
# RUN apt-get install protobuf-compiler -y

RUN pip install -r /app/requirements_strict.txt --no-deps \
    && rm -rf /root/.cache/pip

COPY . /app/
