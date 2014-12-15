from VBrowser import VBrowser

def printReceipt(vBrowser):
    responseObj = httpBin.responseObjs[0];
    responseStr = httpBin.responseStrs[0];
    print("Request returned: %s - %s" % (responseObj.status, responseObj.reason))
    lines = responseStr.split(b"\n")
    for line in range(len(lines)):
        print(lines[line])

httpBin = VBrowser("httpbin.org")

#httpBin.post("/post", params={"username": "joe", "password": "demo", "submit": "Login"})
#printReceipt(httpBin)

httpBin.get("/cookies/set?k1=v1&k2=v2")
printReceipt(httpBin)

httpBin.get("/cookies")
printReceipt(httpBin)

"""
username = input("Username: ")
password = input("Password: ")
"""