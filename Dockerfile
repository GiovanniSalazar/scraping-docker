FROM  ubuntu:18.04 as base
LABEL maintainer="giovani@mail.com.pe"

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

LABEL stage.description="selenium"

RUN apt-get update && apt-get -y install chromium-chromedriver && apt-get -y install curl

RUN cd /tmp && curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh \
	&& sha256sum Anaconda3-2019.03-Linux-x86_64.sh \
	&& bash Anaconda3-2019.03-Linux-x86_64.sh -b

WORKDIR /usr/src/app
COPY . .

ENV PATH=/root/anaconda3/bin:$PATH

RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

ENTRYPOINT ["conda", "run", "-n", "scraping_web", "python", "scraping.py"]
