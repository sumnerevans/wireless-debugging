"""
A WebSocket placeholder class for testing.
"""

class DummySocket:
    """ A dummy WebSocket class.

        Acts as a placeholder for WebSockets for functions that require
        WebSockets. Contains the necessary methods, but provides no actual
        WebSocket functionality. 
    """

    def __init__(self):
        self.sent_messages = []

    def send(self, message):
        """ Tracks the messages sent by send message. """
        self.sent_messages.append(message)

    def receive(self):
        return {
            "messageType": "startSession",
            "apiKey": "f983kDduxhnJDKI22D2Kda",
            "osType": "Android",
            "deviceName": "Google Pixel",
            "appName": "Google Hangouts"
        }

class DummyForm:
    """ A placeholder form that gets inserted into the handle_login function.
    """
    
    def __init__(self):
        self.form_data = {
            'username': 'test@test.com',
        }

    def get(self, item_name):
        """ Grabs a value from form data. """
        return self.form_data.get(item_name)
