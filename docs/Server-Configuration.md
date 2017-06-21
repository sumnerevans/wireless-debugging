# Server Configuration
There are two ways to configure the Wireless Debug server: the command line, and
the `config.yaml` file. Command line arguments override any configuration from a
configuration file.

## Command Line Arguments

    usage: widb_server.py [-h] [-c CONFIG] [--hostname HOSTNAME] [-p PORT]
                      [-u USER_MANAGEMENT_INTERFACE] [-d DATASTORE_INTERFACE]

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            the config file to use (defaults to "config.yaml")
      --hostname HOSTNAME   the hostname to expose the application over
      -p PORT, --port PORT  the port to expose the application on
      -u USER_MANAGEMENT_INTERFACE, --user-management-interface USER_MANAGEMENT_INTERFACE
                            the User Management Interface to use
      -d DATASTORE_INTERFACE, --datastore-interface DATASTORE_INTERFACE
                            the Datastore Interface to use

**Note for Docker:** You can pass these arguments after specifying the container
to run:

    docker run -p 80:80 jsve/wireless-debugging -d 'mongo_datastore_interface.MongoDatastoreInterface()'

## Configuration File
The configuration file must be in YAML format. The default configuration file is
`config.yaml`. A sample configuration file is provided in
`server/sample-config.yaml` Here is an example `config.yaml` file:

    hostname: 0.0.0.0
    port: 80
    datastore_interface: no_datastore_interface.NoDatastoreInterface()
    user_management_interface: email_auth.EmailAuth()
