import http.client, urllib.parse


class VBrowser:
    """A virtual browser class"""

    def __init__(self, host):
        self.host = host
        self.connection = http.client.HTTPSConnection(host)
        self.headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.responseObjs = []
        self.responseStrs = []

    def request(self, path, method, params):
        params = urllib.parse.urlencode(params)
        self.connection.request(method, path, params, self.headers)
        response = self.connection.getresponse()
        self.responseObjs.insert(0, response)
        self.responseStrs.insert(0, response.read())
        return self.responseStrs[0]

    def get(self, path, params={}):
        return self.request(path, "GET", params=params)

    def post(self, path, params={}):
        return self.request(path, "POST", params=params)

