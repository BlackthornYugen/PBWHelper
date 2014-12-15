import http.client, urllib.parse, http.cookies


class VBrowser:
    """A virtual browser class"""

    def __init__(self, host):
        self.host = host
        self.cookies = http.cookies.SimpleCookie()
        self.connection = http.client.HTTPSConnection(host)
        self.headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.responseObjs = []
        self.responseStrs = []

    def request(self, path, method, params):
        params = urllib.parse.urlencode(params)
        self.connection.request(method, path, params, self.headers)
        response = self.connection.getresponse()
        headerItems = response.headers.items()
        for i in range(len(headerItems)):
            if "Set-Cookie" == headerItems[i][0]:
                self.cookies.load(headerItems[i][1])
                self.headers["Cookie"] = self.cookies.output(attrs=[], header="")
        self.responseObjs.insert(0, response)
        self.responseStrs.insert(0, response.read())
        return response.status

    def get(self, path, params={}):
        return self.request(path, "GET", params=params)

    def post(self, path, params={}):
        return self.request(path, "POST", params=params)

