FROM python:3.9.5-slim

LABEL maintainer="MainKronos"


RUN export DEBIAN_FRONTEND=noninteractive; \
    apt-get update; \
    apt-get -y upgrade; \
    apt-get -y install --no-install-recommends; \
    apt-get -y install curl; \
    apt-get -y install tzdata; \
    apt-get -y install locales && locale-gen it_IT.UTF-8; \
    apt-get clean; \
    apt-get autoclean; \
    rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 dockeruser
RUN useradd --no-log-init -r -m --gid dockeruser --uid 1000 dockeruser 

RUN pip3 install --no-cache-dir --upgrade pip

RUN pip3 install config --upgrade --no-cache-dir

COPY requirements.txt /tmp/

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

RUN mkdir /downloads
RUN mkdir /script

WORKDIR /script

COPY config/ /script/

RUN chmod 777 /downloads -R 
RUN chmod 777 /script -R 

RUN sed -i -e 's/# it_IT.UTF-8 UTF-8/it_IT.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=it_IT.UTF-8

ENV WERKZEUG_RUN_MAIN true
ENV FLASK_ENV production
ENV PIP_ROOT_USER_ACTION ignore

# USER dockeruser
ENV USER_NAME dockeruser

ENV VERSION "1.8.1"

EXPOSE 5000

VOLUME [ "/downloads", "/script/json", "/script/connections" ]

CMD ["/script/start.sh"]