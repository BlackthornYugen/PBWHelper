from VBrowser import VBrowser

httpBin = VBrowser("httpbin.org")

username = input("Username: ")
password = input("Password: ")

input("Press Enter to continue")
resp = httpBin.get("/cookies/set?k1=v1&k2=v2")
httpBin.printReceipt()

input("Press Enter to continue")
if resp == 302:
    httpBin.get(httpBin["Location"])
    httpBin.printReceipt()