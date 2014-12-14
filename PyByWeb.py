from VBrowser import VBrowser
import urllib.parse

host = "httpbin.org"
httpBin = VBrowser(host)
params = urllib.parse.urlencode({"username": "joe", "password": "demo", "submit": "Login"})
response = httpBin.post("/post", params=params)

#print(response)
lines = response.split(b"\n")
for line in range(len(lines)):
    print(lines[line])

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