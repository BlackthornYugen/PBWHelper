from VBrowser import VBrowser

host = "httpbin.org"
httpBin = VBrowser(host)

httpBin.get("/get", params={"a": "b"})
print(httpBin.responses[0])
"""
username = input("Username: ")
password = input("Password: ")

params = urllib.parse.urlencode({"username": username, "password": password, "submit": "Login"})
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
path = "/login/process"
#path = "/post"
conn.request("POST", path, params, headers)

r1 = conn.getresponse()
print(r1.status, r1.reason)
data = r1.read()
lines = data.split(b'\n')
for i in range(len(lines)):
    print(lines[i])
"""