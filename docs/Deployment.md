# Deployment

These are the instructions for deploying the web server. Installation
instructions are available for several platforms.

## Deploying on Your Own Machine

### Docker (Recommended)
**Note:** You may have to prepend `sudo` on these commands to run them with
elevated privileges.

**Note:** See [Server Configuration](Server-Configuration) for details on how to
use the CLI.

1. Install Docker.
2. Pull the [Docker image](https://hub.docker.com/r/jsve/wireless-debugging/):
   `docker pull jsve/wireless-debugging`
3. Run the Docker image: `docker run -p 80:80 jsve/wireless-debugging`

### Manual Installation
1. Install Python 3, Pip3, and Ruby.
2. Clone the repository

       git clone https://github.com/sumnerevans/wireless-debugging.git

3. In the `server` directory run the following commands:

       pip3 install -r requirements.txt
       gem install **panini.gem**
       compass compile

4. Run the server using `sudo ./widb_server.py`. **Note:** See [Server
   Configuration](Server-Configuration) for details on how to use the CLI.
5. Verify that the server is running by going to `localhost` in your browser.

## Deploying Onto Cloud Platforms

### AWS
1. Start an EC2 instance running your preferred Linux platform. See [Getting
   Started with Amazon EC2 Linux
   Instances](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html).
2. Follow either the Docker or Manual Installation instructions.

### Google Compute Engine
1. Start a Compute Engine VM instance running your preferred Linux platform. See
   [Creating and Starting an
   Instance](https://cloud.google.com/compute/docs/instances/create-start-instance).
2. Follow either the Docker or Manual Installation instructions.
