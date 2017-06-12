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
    
    def __init__(self, form_data={}):
        self.form_data = form_data

    def get(self, item_name):
        """ Grabs a value from form data. """
        return self.form_data.get(item_name)


class DummyRequest:
    """ A dummy Bottle request object class.

        Acts as a placeholder for the request object fromthe bottle library,
        whose functionality requires a web browser. Contains the necessary
        methods and variables to simulate cookies and forms.

        class members:
            cookies: Dict of String -> String, a dictionary of cookie names to
                cookie values. 
    """

    def __init__(self, cookie=None):
        """ Builds a request object.

        Args:
            cookie:
                Two possible types.
                None, (default) indicates that there are no cookies to start.
                String, sets the cookie named 'api_key' to what was passed into
                    cookie.
        """
        if not cookie:
            self.cookies = {}
        else:
            self.cookies = {
                'api_key': cookie,
            }

        self.forms = DummyForm()



    def add_form(self, form):
        """ Appends a form to a request object.

        Args:
            form: A dummy form object.
        Returns:
            Nothing.

        Modifies the forms class member.
        """
        self.forms = form

    def get_cookie(self, cookie_name):
        """ Gets a cookie from the dictionary of cookies.

        The class member cookies is used in this function.

        Args:
            cookie_name: String, the name of the cookie.
        Returns:
            cookie_value: String, the value contained in the cookie.
        """
        if cookie_name not in self.cookies:
            return None

        return self.cookies.get(cookie_name, '')

    def set_cookie(self, cookie_name, cookie_value):
        """ Sets a cookie in the dictionary of cookies.

        Args:
            cookie_name: String, the name of the cookie.
            cookie_value: String, the value in the cookie.
        Returns:
            Nothing.
        """
        self.cookies[cookie_name] = cookie_value