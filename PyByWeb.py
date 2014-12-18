import subprocess
import re
import requests
import rarfile

# Settings
turn_archive_file = "playerTurn.rar"
download_chunk_size = 10

default_game_name = "elemental"
default_pbw_user = "pbwUser"
default_pbw_pass = "pbwPass"
default_empire_index = "1"
default_empire_pass = "empirePass"

# Print URL Hook Function
def print_url(r, *args, **kwargs):
    print("LOADED URL: \"%s\"" % r.url)


# Null Replacement Function
def choice(prompt, val, hide_default=False):
    if hide_default:
        var = input("%s (***): " % prompt)
    else:
        var = input("%s (%s): " % (prompt, val))
    if var is None or var == "":
        return val
    return var

# Create Session Object
pbw = requests.Session()
pbw.hooks = {"response": print_url}

# Get user/pass from user
username = choice("Username", default_pbw_user)
password = choice("Password", default_pbw_pass, True)

# Authenticate with PBW
resp = pbw.post("https://pbw.spaceempires.net/login/process",
                data=dict(username=username, password=password, submit="login"), timeout=5)

if resp.status_code == 400:
    print("Authentication Failed")
else:
    # Download Turn File (RAR)
    game_name = choice("Game Name", default_game_name)
    resp = pbw.get("http://pbw.spaceempires.net/games/%s/player-turn/download" % game_name, stream=True)

    # Write turn rar file to disk
    with open(turn_archive_file, 'wb') as fd:
        for chunk in resp.iter_content(download_chunk_size):
            fd.write(chunk)
        fd.close()
    print("Rar file downloaded.")

    if not rarfile.is_rarfile(turn_archive_file):
        print("Turn file is not a valid RAR archive.")
    else:
        # Extract to savegame folder
        archive = rarfile.RarFile(turn_archive_file)
        turn_file = archive.infolist()[0]
        archive.extract(turn_file)
        print("Turn file extracted. Launching Space Empires IV.")
        with open(turn_file.filename, "rb") as fd:
            binary_data = fd.read(2000)
            unicode_data = binary_data.decode("utf-8", errors="ignore")
            fd.close()
        columns = "%-5s %-34s %-30s %-35s %s"
        pattern = re.compile(r"(\d)\s{5,}(.+?)\s{5,}(.+?)\s*?(\S*?)(Alive|Dead)")
        print(columns % ("", "Empire Name", "Leader", "Email", "Status"))
        print(columns % ("", "-------------------------------", "----------------------------", "--------------------------------", "------"))
        for empire in pattern.findall(unicode_data):
            print(columns % empire)

        empire_index = choice("Empire Index", default_empire_index)
        empire_password = choice("Empire Password", default_empire_pass, True)
        print("Launching Space Empires IV. This may take a few moments.")
        process_exit_id = subprocess.Popen(["Se4.exe", turn_file.filename, empire_password, empire_index, ' ']).wait()
        if process_exit_id == 2:
            print("Empire index or Empire password invalid. Try again?")
            # TODO: Offer to let the user enter new empire info and try again
        else:
            print("Space Empires has been closed. Uploading file.")
            with open("./savegame/%s_000%s.plr" % (game_name, empire_index), "rb") as fd:
                resp = pbw.post("http://pbw.spaceempires.net/games/%s/player-turn/upload" % game_name,
                                files={"plr_file": fd}, allow_redirects=False)
                fd.close()
            if resp.status_code not in range (200,399):
                print("Failed to upload plr file.")
            else:
                print("Successfully uploaded plr file.")

print("Exiting.")
pbw.close()
# TODO: Figure out why I need to call exit, it should just exit here unless I didn't close/end something...
exit()