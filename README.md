# Wireless Debugging
WiDebug (widb)

## Development Environment Setup

### Web Server
1. Ensure python 3 and Cloud SDK with Bundled Python is installed
 
2. Run the following commands to install the necessary SASS plugins:

        gem install compass
        gem install font-awesome-sass
        gem install bootstrap-sass

3. Install the following Python libraries. (`pip3 install` is probably the easiest way to
   do this.)
   You can also run 'pip install -r requirements.txt' while in the main directory. Also run 'pip3 install -r requirements.txt' 
        kajiki
        bottle
        markupsafe
        requests
        gevent
        gevent-websocket
        PyYaml

4. Run `compass compile`  in the directory with the config.rb file (/server) 

5. To setup local, run commands:
`pip3 install virtualenv`
in /server dir: `virtualenv env`
`.\env\Scripts\activate`
`pip3 install -r requirements.txt`
run `python widb_server.py` and will see it on `localhost:8080`  
for more information: `https://cloud.google.com/appengine/docs/flexible/python/quickstart#before-you-begin` 

6. deploy: `gcloud app deploy --project <project-id> --version <version-id>` 
will be shown on `www.<project-id>.appspot.com`

## Contributors
- Jonathan Sumner Evans
- Amanda Giles
- Reece Hughes
- Daichi Jameson
- Tiffany Kalin
