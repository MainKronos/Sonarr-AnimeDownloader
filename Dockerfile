FROM ubuntu:18.04

MAINTAINER MainKronos

RUN mkdir /script
RUN apt-get update -y

RUN apt-get install -y python3 python3-pip cron ffmpeg nano wget -y

RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata

RUN apt-get install -y locales && locale-gen it_IT.UTF-8

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

# CMD ["cron", "-f"]
CMD ["python3","-u","/script/main.py"]