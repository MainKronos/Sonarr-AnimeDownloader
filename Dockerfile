FROM python:3.9.5-slim

LABEL maintainer="MainKronos"

RUN mkdir /script

RUN export DEBIAN_FRONTEND=noninteractive; \
    apt-get update; \
    apt-get -y upgrade; \
    apt-get -y install --no-install-recommends; \
    apt-get -y install ffmpeg; \
    apt-get -y install tzdata; \
    apt-get -y install locales && locale-gen it_IT.UTF-8; \
    apt-get clean; \
    apt-get autoclean; \
    rm -rf /var/lib/apt/lists/*

WORKDIR /script
RUN pip3 install --upgrade pip

RUN pip3 install config --upgrade

COPY requirements.txt /tmp/

RUN pip3 install -r /tmp/requirements.txt

COPY config/json/* /script/json/
COPY config/main.py /script/
COPY config/app/. /script/app/

RUN locale-gen it_IT.UTF-8
ENV LANG it_IT.UTF-8
ENV LANGUAGE it_IT:en
ENV LC_ALL it_IT.UTF-8

ENV VERSION "1.4.4"

EXPOSE 5000

CMD ["python3","-u","/script/main.py"]