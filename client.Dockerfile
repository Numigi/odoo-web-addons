FROM debian:stretch
LABEL maintainer="numigi <contact@numigi.com>"

RUN apt-get update && apt-get install -y \
        curl \
        build-essential \
        libssl-dev && \
    curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get install -y nodejs

RUN useradd -ms /bin/bash client
WORKDIR /home/client
USER client

COPY package.json .
RUN npm install

COPY .ava .ava
COPY  web_contextual_search_favorite web_contextual_search_favorite
