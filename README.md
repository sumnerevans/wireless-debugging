# Wireless Debugging
WiDebug (widb)

## Development Environment Setup
1. Ensure python 3 is installed 

2. cd to the `server` directory 

3. Run the following commands to install the necessary SASS plugins:

        gem install compass
        gem install font-awesome-sass
        gem install bootstrap-sass

4. Install the following Python libraries. (`pip install` is probably the easiest way to
   do this.)
   You can also run `pip install -r requirements.txt` 
        kajiki
        bottle
        markupsafe
        requests
        gevent
        gevent-websocket
        PyYaml  

5. Run `compass compile` 

6. Run the web application by running `widb_server.py` and navigating in your browser to `localhost:8080`

## Web Server Setup with Development Environment 
1. Ensure python 3 and Cloud SDK with Bundled Python is installed

2. cd to the `server` directory
 
2. Run the following commands to install the necessary SASS plugins:

        gem install compass
        gem install font-awesome-sass
        gem install bootstrap-sass

3. Install the following Python libraries. (`pip3 install` is probably the easiest way to
   do this.)
   You can also run 'pip install -r requirements.txt' 
   Also run 'pip3 install -r requirements.txt' 
        kajiki
        bottle
        markupsafe
        requests
        gevent
        gevent-websocket
        PyYaml

4. Run `compass compile`   

5. To setup local web server app engine instance, run commands:
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
