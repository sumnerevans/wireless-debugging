FROM ubuntu:16.04
MAINTAINER Sumner Evans

# Create the MongoDB data directory
RUN mkdir -p /data/db

# Update the system
RUN apt-get update && apt-get install -y python3 python3-pip ruby ruby-compass

# Create a Bottle user.
RUN groupadd web
RUN useradd -d /home/bottle -m bottle

# Add the source files to the user.
WORKDIR /home/bottle
ADD https://github.com/sumnerevans/wireless-debugging/archive/master.zip .
RUN unzip master.zip

# Change into the server directory
WORKDIR /home/bottle/wireless-debugging-master/server

# Install the necessary packages.
RUN gem install compass font-awesome-sass bootstrap-sass
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Compile the CSS.
RUN compass compile

# Expose port 80 and run the application.
EXPOSE 80
CMD ["/home/bottle/wireless-debugging-master/server/widb_server.py"]
