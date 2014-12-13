import http.client, urllib.parse

class VBrowser:
    """A virtual browser class"""
    def __init__(self, host):
        self.host = host
        self.connection = http.client.HTTPSConnection(host)
        self.params = {}
        self.headers = {}
        self.responses = []

    def request(self, path, method):
        self.connection.request(method, path, self.params, self.headers)
        response = self.connection.getresponse()
        self.responses.insert(0, response)
        return response.read()

    def get(self, path):
        return self.request(path, "GET")

    def post(self, path):
        return self.request(path, "POST")

