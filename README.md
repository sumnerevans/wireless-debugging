# Wireless Debugging
WiDebug (widb)

## Development Environment Setup

### Web Server
1. Run the following commands to install the necessary SASS plugins:

        gem install compass
        gem install font-awesome-sass
        gem install bootstrap-sass

2. Install the following Python libraries. (Pip is probably the easiest way to
   do this.)

        kajiki
        bottle
        markupsafe
        requests
        gevent
        gevent-websocket
        PyYaml

3. Run `compass compile`

4. Run the app by running `server/widb_server.py` and navigating in your browser
   to `localhost:8080`

## Contributors
- Jonathan Sumner Evans
- Amanda Giles
- Reece Hughes
- Daichi Jameson
- Tiffany Kalin
