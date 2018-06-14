FROM debian:stretch
MAINTAINER numigi <contact@numigi.com>

RUN useradd -ms /bin/bash client
WORKDIR /home/client

RUN apt-get update && apt-get install -y \
        curl \
        build-essential \
        libssl-dev && \
    curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

USER client

COPY package.json .
RUN npm install --only=dev

COPY .ava .ava
COPY  web_contextual_search_favorite web_contextual_search_favorite
