import requests, rarfile

# Settings
turn_archive_file = "playerTurn.rar"
download_chunk_size = 10

# Print URL Hook Function
def print_url(r, *args, **kwargs):
    print("\nLOADED URL: \"%s\"" % r.url)

# Null Replacement Function
def if_null(var, val):
  if var is None or var == "":
    return val
  return var

# Create Session Object
pbw = requests.Session()
pbw.hooks = {"response": print_url}

# Get user/pass from user
username = if_null(input("Username: "), "defaultUser")
password = if_null(input("Password: "), "defaultPass")

# Authenticate with PBW
resp = pbw.post("https://pbw.spaceempires.net/login/process",
                data=dict(username=username, password=password, submit="login"), timeout=5)

# Print the response
print(resp.text)
print(resp.status_code)
print(resp.url)

if resp.status_code == 400:
    print("Authentication Failed")
else:
    # Download Turn File (RAR)
    resp = pbw.get("http://pbw.spaceempires.net/games/elemental/player-turn/download", stream=True)
    print(resp.status_code)

    # Write turn rar file to disk
    with open(turn_archive_file, 'wb') as fd:
        for chunk in resp.iter_content(download_chunk_size):
            fd.write(chunk)

    # Verify that it is a valid RAR file (UNRAR MUST BE IN PATH)
    if rarfile.is_rarfile(turn_archive_file):
        print("Rar file downloaded.")
        rarfile.RarFile(turn_archive_file).extractall()
        print("Turn file extracted.")
    else:
        print("Turn file is not a valid RAR archive.")