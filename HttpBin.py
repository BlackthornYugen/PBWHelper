from VBrowser import VBrowser

httpBin = VBrowser("httpbin.org")


def if_null(var, val):
  if var is None or var == "":
    return val
  return var

username = if_null(input("Username: "), "defaultUser")
password = if_null(input("Password: "), "defaultPass")

"""
input("Press Enter to continue")
resp = httpBin.get("/cookies/set?k1=v1&k2=v2")
httpBin.printReceipt()

input("Press Enter to continue")
if resp == 302:
    httpBin.get(httpBin["Location"])
    httpBin.printReceipt()
"""
def print_url(r, *args, **kwargs):
    print("\nLOADED URL: \"%s\"" % r.url)

from requests.auth import AuthBase

import requests

httpBin = requests.Session()
httpBin.hooks = {"response": print_url}
httpBin.headers.update({"submit": "login"})
r = httpBin.post("https://httpbin.org/post", data={"username":username, "password":password, "submit": "login"})
print(r.text)
