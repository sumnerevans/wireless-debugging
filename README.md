# Wireless Debugging
WiDebug (widb)

## Development Environment Setup

### Web Server
1. Ensure python 3 is installed
 
2. Run the following commands to install the necessary SASS plugins:

        gem install compass
        gem install font-awesome-sass
        gem install bootstrap-sass

3. Install the following Python libraries. (`pip3 install` is probably the easiest way to
   do this.)

        kajiki
        bottle
        markupsafe
        requests
        gevent
        gevent-websocket
        PyYaml

4. Run `compass compile`  in the directory with the config.rb file (/server) 

5. Run the app by running `widb_server.py` and navigating in your browser
   to `localhost:8080`

## Contributors
- Jonathan Sumner Evans
- Amanda Giles
- Reece Hughes
- Daichi Jameson
- Tiffany Kalin
