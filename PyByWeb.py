from VBrowser import VBrowser

pbw = VBrowser("pbw.spaceempires.net")

username = input("Username: ")
password = input("Password: ")

resp = pbw.post("/login/process", params={"username":username, "password":password, "submit": "login"})
pbw.printReceipt()

pbw.get("/dashboard")
pbw.printReceipt()

pbw.get("/games/elemental")
pbw.printReceipt()