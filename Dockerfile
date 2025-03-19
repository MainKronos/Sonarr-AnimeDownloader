FROM python:3.13.2-slim

LABEL maintainer="MainKronos"

RUN export DEBIAN_FRONTEND=noninteractive; \
	apt-get update; \
	apt-get -y upgrade; \
	apt-get -y install --no-install-recommends; \
	apt-get -y install curl; \
	apt-get -y install ffmpeg; \
	apt-get -y install rtmpdump; \
	apt-get -y install tzdata; \
	apt-get -y install build-essential; \
	apt-get -y install locales && locale-gen it_IT.UTF-8; \
	apt-get clean; \
	apt-get autoclean; \
	rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 dockeruser
RUN useradd --no-log-init -r -m --gid dockeruser --uid 1000 dockeruser 

RUN pip3 install --no-cache-dir --upgrade pip

RUN pip3 install config --upgrade --no-cache-dir

COPY src/requirements.txt /tmp/

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

RUN mkdir /downloads
RUN mkdir /src

WORKDIR /src

COPY src/ /src/

RUN chmod 777 /downloads -R 
RUN chmod 777 /src -R 

RUN gcc /src/start.c -o /start.bin
RUN rm /src/start.c
RUN chown root:root /start.bin
RUN chmod 6751 /start.bin

RUN sed -i -e 's/# it_IT.UTF-8 UTF-8/it_IT.UTF-8 UTF-8/' /etc/locale.gen && \
	dpkg-reconfigure --frontend=noninteractive locales && \
	update-locale LANG=it_IT.UTF-8

ENV FLASK_DEBUG production
ENV PIP_ROOT_USER_ACTION ignore

# USER dockeruser
ENV USER_NAME dockeruser

ARG set_version="dev"
ENV VERSION=$set_version

EXPOSE 5000

VOLUME [ "/downloads", "/src/script", "/src/database" ]

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl --fail http://localhost:5000 || exit 1

CMD ["/start.bin"]
