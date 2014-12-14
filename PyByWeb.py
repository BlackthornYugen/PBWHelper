from VBrowser import VBrowser

httpBin = VBrowser("httpbin.org")
response = httpBin.post("/post", params={"username": "joe", "password": "demo", "submit": "Login"})

#print(response)
lines = response.split(b"\n")
for line in range(len(lines)):
    print(lines[line])

"""
username = input("Username: ")
password = input("Password: ")
"""