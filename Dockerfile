FROM ubuntu:16.04
MAINTAINER Sumner Evans

# Install the necessary packages.
RUN apt-get update && apt-get install -y python3 python3-pip ruby ruby-compass
RUN gem install compass font-awesome-sass bootstrap-sass
RUN pip3 install --upgrade pip
RUN pip3 install kajiki bottle markupsafe requests gevent gevent-websocket PyYaml

# Create the MongoDB data directory
RUN mkdir -p /data/db

# Create a Bottle user.
RUN groupadd web
RUN useradd -d /home/bottle -m bottle

# Add the source files to the user.
WORKDIR /home/bottle
ADD https://github.com/sumnerevans/wireless-debugging/archive/master.zip .
RUN unzip wireless-debugging-master.zip

# Compile the CSS.
WORKDIR /home/bottle/server
RUN compass compile

# Expose port 80 and run the application.
EXPOSE 80
CMD ["/home/bottle/server/widb_server.py"]
