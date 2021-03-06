# User Management Interface
## Overview
The user management interface is what determines where mobile devices send their
logs. The interface defines how the user is identified, how their API Key is
generated, how their API key is stored, and who receives logs from which mobile
devices. This enables the user to tailor the server to their needs, whether it
be security, scalability, or convenience.

More details of the User Management Interface may be found in the [Design
Document](https://TODO.Goto.docs).

## Interactions
- When the user goes to the Wireless Debug website, the User Management
  Interface is called to determine whether or not the user is logged in.
- If they are not logged in, the User Management Interface will need to generate
  HTML for the the login functionality.
- The User Management Interface will need to handle the login, and generate an
  API key for the user.
- When the server is sending logs to the Web UIs, the User Management Interface
  will need to determine which Web UIs the logs should be sent to.
- User Management Interface methods are used in the following files:
    - `controller/root.py`
    - `controller/websocket.py`

## Implementation
In order to implement a user management interface, the following functions must
be implemented:

**`get_login_ui()`**
- **Purpose:** generate an HTML UI to show on the login page.
- **Arguments:**
    - None
- **Returns:** a string with the HTML for the login UI. This HTML should include
  an HTML form which posts to the login URL (See Section 6.2).
 
**`is_user_logged_in(request)`**
- **Purpose:** determines if the user is already authenticated.
- **Arguments:**
    - `request`: the HTTP request context from Bottle
- **Returns:** `True` if the user is authenticated, `False` otherwise
 
**`handle_login(form_data, request, response)`**
- **Purpose:** perform server-side user authentication.
- **Arguments:**
    - `form_data`: the form data from the form generated by get_login_ui.
    - `request`: the HTTP request context from Bottle
    - `response`: the HTTP response context from Bottle
- **Returns:** A tuple containing:
    - `login_successful`: a boolean indicating if the login was successful or not.
    - `error_message`: a string containing the error message if the login
      failed. If login_successful is true, this can return either a blank string
      or log message to describe anything important.
- **Note:** this function can set cookies on the response object
 
**`get_api_key_for_user(request)`**
- **Purpose:** returns the API Key associated with the request.
- **Arguments:**
    - `request`: the HTTP request context from Bottle
- **Returns:** the API Key associated with the given request. The request
  parameter can be used to access any cookies that may have been set in
  `handle_login`.
- **Note:** this function can retrieve cookie values using the request object
 
**`find_associated_websockets(api_key, websocket_connections)`**
- **Purpose:** determines which WebSocket connections to send parsed logs to.
- **Arguments:**
    - `api_key`: the API Key for which to find associated sessions
    - `websocket_connections`: a list of WebSocket connections to Web UIs
      connected to the Web App Backend
- **Returns:** a list of WebSocket connections to send the logs to (this should
  be a subset of the `websocket_connections` list).
