import os


def get_zip_location():
    while True:
        ziploc = input("Enter The ZIP file LOCATION : ")
        if ziploc.split("/")[-1].find(".zip") == -1:
            print("Invalid Location")
            continue
        break
    return ziploc


def get_pass():
    password = input("[sudo] password for user: ")
    return password


def execute_cmd(sudoPassword, command):
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))


def unzip_module(passw, zip_file):
    command = "unzip %s -d /usr/local/lib/" % zip_file
    execute_cmd(passw, command)


def create_desktop(passw, zip_loc):
    folder_name = zip_location.split("/")[-1].split(".")[0]
    cmd = "[Desktop Entry]\nVersion = 1.0\nName = Manage Odoo\nComment = Abhinav Product\nExec =/bin/bash -c " \
          "'python3 /usr/local/lib/%(s)s/main.py'\nPath =/usr/local/lib/%(s)s/\nTerminal = true\nType = " \
          "Application" \
          "\nCategories = Utility;Application;" % {'s': folder_name}

    file = open("manage_odoo.desktop", "w")
    file.write(cmd)
    file.close()
    os.system('echo %s|sudo -S %s' % (passw, 'mv manage_odoo.desktop /usr/share/applications/'))
    os.system('echo %s|sudo -S %s' % (passw, 'pip3 install tk'))


def run():
    password = get_pass()
    zip_loc = get_zip_location()
    unzip_module(password, zip_loc)
    create_desktop(password, zip_loc)


if __name__ == "__main__":
    run()
