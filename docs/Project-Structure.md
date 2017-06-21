# Project Structure
## Directory Structure
- `/`: the project root. This contains Docker configurations, Travis CI
  configurations, the `.gitignore` and some project information.
    - `docs`: contains PDFs of the original documents created for the field
      session class.
    - `mobile`: contains the source code for the mobile APIs and sample
      applications.
        - `android/WirelessDebugger`
            - `SampleApp`: source code for the sample application.
            - `wirelessdebugger`: source code for the Wireless Debugger library.
        - `ios/WirelessDebug`
            - `WirelessDebug`: source code for the sample application.
            - `WirelessDebugger`: source code for the Wireledd Debugger library.
    - `server`: the source code for the server component:
        - `controller`: the Bottle router functions
        - `datastore_interfaces`: the [Datastore Interface](Datastore-Interface)
          implementations
        - `helpers`: utility functions and classes
        - `parsing_lib`: the [Parsing Library](Parsing-Library)
        - `resources`: SCSS and font resources
        - `template`: the Kajiki page templates
        - `tests`: the Python tests
        - `user_management_interfaces`: the [User Management
          Interface](User-Management-Interface) implementations

## Server Technology Stack Overview
The server has controllers and views (templates) and, interface implementations,
and the parsing library.

- The templates are [Kajiki XML
  templates](http://pythonhosted.org/Kajiki/xml-templates.html).
- The controllers use the [Bottle](http://bottlepy.org/docs/dev/) web
  micro-framework to route requests to the correct Python functions.
- The interface implementations are written in Python.
- The project uses [SASS](http://sass-lang.com/) and compiles it to CSS.
