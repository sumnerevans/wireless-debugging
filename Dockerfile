FROM ubuntu
MAINTAINER Sumner Evans

RUN apt-get update && apt-get install -y python3 python3-pip ruby ruby-compass

RUN gem install compass font-awesome-sass bootstrap-sass
RUN pip3 install --upgrade pip
RUN pip3 install kajiki bottle markupsafe requests gevent gevent-websocket PyYaml

# create user
RUN groupadd web
RUN useradd -d /home/bottle -m bottle

WORKDIR /home/bottle
ADD https://cdn.the-evans.family/wireless-debugger.zip .
RUN unzip wireless-debugger.zip
ADD https://cdn.the-evans.family/config.yaml .
WORKDIR /home/bottle/server
RUN compass compile

EXPOSE 80
# ENTRYPOINT ["ls", "/home/bottle/wireless-debugging"]
ENTRYPOINT ["/usr/bin/python3", "/home/bottle/server/widb_server.py"]
