FROM node:9.11.2-stretch
MAINTAINER numigi <contact@numigi.com>

RUN useradd -ms /bin/bash client
WORKDIR /home/client

USER client

COPY .docker_files/package.json .
RUN npm install

COPY .docker_files/ava ava
COPY  web_contextual_search_favorite web_contextual_search_favorite
