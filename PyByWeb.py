import subprocess, re, requests, rarfile, json, os, contextlib, time

# Settings
turn_archive_file = "playerTurn.rar"
download_chunk_size = 10
settings_file = "PyByWeb.json"
certificate_file = "cacert.pem"

# If cacert.pem exists; use it! Otherwise offer to let user continue without SSL.
if os.path.isfile(certificate_file):
    verify = certificate_file
else:
    print('Certificate file "%s" was not found!' % certificate_file)
    if input('Enter "Yes" to continue without SSL: ').lower().strip() != "yes":
        input("Press enter to exit.")
        exit()
    verify = False

# If settings file doesn't exist, make it.
if not os.path.isfile(settings_file):
    with open(settings_file, "w") as fd:
        fd.write(('{\n'
                  '  "game_name" : "elemental",\n'
                  '  "pbw_user" : "pbwUser",\n'
                  '  "pbw_pass": "pbwPass",\n'
                  '  "empire_index" : "1",\n'
                  '  "empire_pass" : "empirePass",\n'
                  '  "confirm_with_user" : true\n'
                  '}'
        ))

# Load settings.json
with open(settings_file) as fd: settings = json.loads(fd.read())

# Print URL Hook Function
def print_url(r, *args, **kwargs): print("LOADED URL: \"%s\"" % r.url)


# Null Replacement Function
def choice(prompt, val, hide_default=False):
    if not settings["confirm_with_user"]:
        return val
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
username = choice("Username", settings["pbw_user"])
password = choice("Password", settings["pbw_pass"], True)

# Authenticate with PBW
resp = pbw.post("https://pbw.spaceempires.net/login/process",
                data=dict(username=username, password=password, submit="login"),
                timeout=5, verify=verify)

if resp.status_code == 400: print("Authentication Failed")
else:
    # Download Turn File (RAR)
    game_name = choice("Game Name", settings["game_name"])
    resp = pbw.get("http://pbw.spaceempires.net/games/%s/player-turn/download" % game_name, stream=True)

    # Write turn rar file to disk
    with contextlib.suppress(FileNotFoundError): os.remove(turn_archive_file)
    with open(turn_archive_file, 'wb') as fd:
        for chunk in resp.iter_content(download_chunk_size):
            fd.write(chunk)
    print("Rar file downloaded.")

    if not rarfile.is_rarfile(turn_archive_file): print("Turn file is not a valid RAR archive.")
    else:
        # Extract to savegame folder
        archive = rarfile.RarFile(turn_archive_file)
        turn_file = archive.infolist()[0]
        archive.extract(turn_file)
        print("Turn file extracted.")
        with open(turn_file.filename, "rb") as fd:
            binary_data = fd.read(2000)
            unicode_data = binary_data.decode("utf-8", errors="ignore")
        columns = "%-5s %-34s %-30s\n      %-34s %s"
        pattern = re.compile(r"(\d)\s{5,}(.+?)\s{5,}(.+?)\s*?(\S*?)(Alive|Dead)")
        print("\n", columns % ("", "Empire Name", "Leader", "Email", "Status"), sep="")
        horizontal_ruler = " " * 6 + "-" * 65
        print(horizontal_ruler)
        for empire in pattern.findall(unicode_data): print(columns % empire, horizontal_ruler, sep="\n")
        empire_index = choice("Empire Index", settings["empire_index"])
        empire_password = choice("Empire Password", settings["empire_pass"], True)
        se_process = subprocess.Popen(["Se4.exe", turn_file.filename, empire_password, empire_index, ' '])
        print("Launching Space Empires IV.")
        message = '"Se4.exe" is running'
        while se_process.poll() is None:
            print("\r   ", " " * len(message), "\r", message, end="", sep="", flush=True)
            for i in range(3):
                print(".", sep="", end="", flush=True)
                if se_process.poll() is None: time.sleep(1)
        print()
        if se_process.poll() == 2:
            print("Empire index or Empire password invalid.")
        else:
            print("Space Empires has been closed.")
            try:
                with open("./savegame/%s_000%s.plr" % (game_name, empire_index), "rb") as fd:
                    resp = pbw.post("http://pbw.spaceempires.net/games/%s/player-turn/upload" % game_name,
                                    files={"plr_file": fd}, allow_redirects=False)
                if resp.status_code not in range(200, 399):
                    print("Failed to upload plr file.")
                else:
                    print("Successfully uploaded plr file.")
            except FileNotFoundError:
                print('Failed to upload plr file because "%s_000%s.plr" was not found in the savegame folder.'
                      % (game_name, empire_index))
                pass
        with contextlib.suppress(FileNotFoundError): os.remove(turn_file.filename)
    with contextlib.suppress(FileNotFoundError): os.remove(turn_archive_file)
pbw.close()
input("Press Enter to exit.")