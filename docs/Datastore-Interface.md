# Datastore Interface

## Overview
The Datastore Interface specifies a set of functions required in order to
implement historical log storage. The interface defines methods for accessing
and storing session information including devices, app, start time, logs, and
aliases.

## Interactions
- After logs have been parsed, they will be sent to the Datastore Interface
  implementation for storage.
- When the user requests a list of devices, apps, or sessions, the Datastore
  Interface implementation will return the list.
- When the user requests historical logs, the Datastore Interface will retrieve
  the logs.

## Implementation
For a class to implement the Datastore Interface, it will need to define the
following functions.

Any set up operations should occur in the constructor of the Datastore Interface.

Device names and app names can be passed as de-aliased device names and
de-aliased app names, respectively.

**`store_logs(api_key, device_name, app_name, start_time, os_type, log_entries)`**
- **Purpose:** store a set of log entries to the datastore. This function may be
  called multiple times per session, so it must append the log entries in the
  storage mechanism.
- **Arguments:**
    - `api_key`: the API Key associated with the logs
    - `device_name`: the name of the device associated with the logs
    - `app_name`: the name of the app associated with the logs
    - `start_time`: the time that the session started
    - `os_type`: the OS type (iOS or Android)
    - `log_entries`: the log entries to store
 
**`set_session_over(api_key, device_name, app_name, start_time)`**
- **Purpose:** called to indicate to the datastore that the session is over.
  This can set a flag on the session in the datastore indicating that it should
  not be modified, for example.
- **Arguments:**
    - `api_key`: the API Key associated with the logs
    - `device_name`: the name of the device associated with the logs
    - `app_name`: the name of the app associated with the logs
    - `start_time`: the time that the session started
 
**`retrieve_logs(api_key, device_name, app_name, start_time)`**
- **Purpose:** retrieve the logs for a given session.
- **Arguments:**
    - `api_key`: the API Key to retrieve logs for
    - `device_name`: the name of the device to retrieve logs for
    - `app_name`: the name of the app to retrieve logs for
    - `start_time`: the time that the session started
- **Returns:** a dictionary with:
    - `osType`: the OS type
    - `logEntries`: a list of log entries as Python dictionaries
 
**`retrieve_devices(api_key)`**
- **Purpose:** retrieve a list of devices associated with the given API Key.
- **Arguments:**
    - `api_key`: the API Key to retrieve devices for
- **Returns:** a list of devices associated with the given API Key. Each device
  is a dictionary with:
    - `array`: array of the names of the devices
 
**`retrieve_apps(api_key, device_name)`**
- **Purpose:** retrieve a list of apps associated with the given API Key and
  device.
- **Arguments:**
    - `api_key`: the API Key to retrieve apps for
    - `device_name`: the device name to retrieve apps for
- **Returns:**
    - `array (string)`: a list of app names associated with the given device.
 
**`retrieve_sessions(api_key, device_name, app)`**
- **Purpose:** retrieve a list of sessions for a given API Key, device, and app.
- **Arguments:**
    - `api_key`: the API Key to retrieve sessions for
    - `device_name`: the name of the device to retrieve sessions for
    - `app_name`: the name of the app to retrieve sessions for
- **Returns:**
    - `array (datetime objects)`: list of datetime objects, one for each of the
      session start times associated with the given API Key, device, and app.
 
**`add_device_app(api_key, device_name, app)`**
- **Purpose:** add a device/app combination to the device/app collection
- **Arguments:**
    - `api_key`: API Key of user
    - `device_name`: the name of the device
    - `app_name`: the name of the app
 
**`update_alias_device(api_key, device_raw_name, device_alias)`**
- **Purpose:** add a mapping from a device to a device alias.
- **Arguments:**
    - `api_key`: the API Key of the device’s owner
    - `device_raw_name`: the raw device name
    - `device_alias`: the new alias of the device
 
**`update_alias_app(api_key, device_name, app_raw_name, app_alias)`**
- **Purpose:** add a mapping from a device to a device alias.
- **Arguments:**
    - `api_key`: the API Key of the device’s owner
    - `device_name`: the raw device name
    - `app_raw_name`: name being aliased 
    - `app_alias`: the new alias of the app
 
**`get_raw_device_name_from_alias(api_key, device_alias)`**
- **Purpose:** retrieve a raw device name given a device alias.
- **Arguments:**
    - `api_key`: the API Key of the device’s owner
    - `device_alias`: the alias of the device 
- **Returns:** `string`: the raw device name
 
**`get_raw_app_name_from_alias(api_key, device_name, app_alias)`**
- **Purpose:** retrieve a raw device name given a device alias.
- **Arguments:**
    - `api_key`: the API Key of the device’s owner
    - `device_name`: device connected to the app
    - `app_alias`: the alias of the app
- **Returns:** `string`: the raw app name
 
**`clear_datastore()`**
- **Purpose:** clears datastore of records

## Additional Information

- [Design Document](../tree/master/docs/DesignDocument.pdf)
- [Server Library Datastore](../tree/master/docs/ServerLibraryDatastore.pdf)
