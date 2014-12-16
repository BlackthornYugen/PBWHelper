from VBrowser import VBrowser

httpBin = VBrowser("pbw.spaceempires.net")

username = input("Username: ")
password = input("Password: ")

resp = httpBin.post("/login/process", params={"username":username, "password":password, "submit": "login"})
httpBin.printReceipt()

httpBin.get("/dashboard")
httpBin.printReceipt()

httpBin.get("/games/elemental")
httpBin.printReceipt()