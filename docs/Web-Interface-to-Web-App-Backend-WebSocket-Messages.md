# Web Interface to Web App Backend WebSocket Messages
Going from the web interface to the web app backend, there is a single websocket
message that is sent which is used to associate a user to the sent web socket.

## Associate User
- **Message Type:** `associateUser`
- **Payload Type**: JSON
- **Purpose**: when a user logs in to the web interface, this message will be
  sent to the Web App Backend to tell the backend which logs to send to the Web
  Interface.
- **Fields**:
    - `messageType (string)`: The message type of the message, which will be
      `associateUser`.
    - `apiKey (string)`: the API Key from the user defined User Management
      Interface.
- **Example**:

      {
        "messageType": "associateUser",
        "apiKey": "cb572446-21f2-44d0-8983-4cf30300b574"
      }
