# Wireless Debugging
[![Build Status](https://travis-ci.org/sumnerevans/wireless-debugging.svg?branch=master)](https://travis-ci.org/sumnerevans/wireless-debugging)

This is a student project by CS students at Colorado School of Mines. The goal
of this project is to build a mobile SDK and sample web server to allow mobile
app log streaming to a web UI console.

This project was done under supervision of Google and was sponsored by the
Colorado School of Mines for the CSCI-370 course.

## Development Environment Setup
1. Ensure python 3 is installed

2. cd to the `server` directory

3. Run the following commands to install the necessary SASS plugins:

        gem install compass
        gem install font-awesome-sass
        gem install bootstrap-sass

4. Install the following Python libraries. (`pip install` is probably the
   easiest way to do this.) You can also run `pip install -r requirements.txt`

        kajiki
        bottle
        markupsafe
        requests
        gevent
        gevent-websocket
        PyYaml

5. Run `compass compile`

6. Run the web application by running `widb_server.py` and navigating in your
   browser to `localhost:8080`

## Web Server Setup with Development Environment
1. Ensure python 3 and Cloud SDK with Bundled Python is installed

2. cd to the `server` directory

2. Run the following commands to install the necessary SASS plugins:

        gem install compass
        gem install font-awesome-sass
        gem install bootstrap-sass

3. Install the following Python libraries. (`pip3 install` is probably the
   easiest way to do this.) You can also run 'pip install -r requirements.txt'.
   Also run 'pip3 install -r requirements.txt'

        kajiki
        bottle
        markupsafe
        requests
        gevent
        gevent-websocket
        PyYaml

4. Run `compass compile`

5. To setup local web server app engine instance, run the following commands
   from the `server` directory:

        pip3 install virtualenv
        virtualenv env
        .\env\Scripts\activate
        pip3 install -r requirements.txt

    run `python widb_server.py` and will see the app on `localhost:8080`.

    For more information, see [Before you Begin](https://cloud.google.com/appengine/docs/flexible/python/quickstart#before-you-begin)

6. deploy: `gcloud app deploy --project <project-id> --version <version-id>`.

   The app will be shown on `www.<project-id>.appspot.com`

## Contributors
- Jonathan Sumner Evans
- Amanda Giles
- Reece Hughes
- Daichi Jameson
- Tiffany Kalin
