FROM ubuntu:18.04 as base
LABEL maintainer="giovani@mail.com.pe"

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

LABEL stage.description="selenium"

RUN apt-get update && apt-get -y install chromium-chromedriver && apt-get -y install curl

LABEL stage.description="conda"

SHELL ["/bin/bash", "-c"]

RUN cd /tmp && curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh \
	&& sha256sum Anaconda3-2019.03-Linux-x86_64.sh \
	&& bash Anaconda3-2019.03-Linux-x86_64.sh -b

ENV PATH=/root/anaconda3/bin:$PATH

WORKDIR /usr/src/app
COPY . .
RUN chmod +x entrypoint.sh

LABEL stage.description="create environment"

RUN cd /usr/src/app && conda env create -qf environment.yml

RUN activate scraping_web && python /usr/src/app/scraping.py
