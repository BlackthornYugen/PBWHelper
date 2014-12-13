import http.client, urllib.parse

class VBrowser:
    """A virtual browser class"""
    def __init__(self, host):
        self.host = host
        self.connection = http.client.HTTPSConnection(host)
        self.headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.responses = []

    def request(self, path, method, params):
        self.connection.request(method, path, params, self.headers)
        response = self.connection.getresponse()
        self.responses.insert(0, response)
        return response.read()

    def get(self, path, params = {}):
        return self.request(path, "GET", params)

    def post(self, path, params = {}):
        return self.request(path, "POST", params)

