import os
from time import sleep
import shutil
import requests
from zipfile import ZipFile
import subprocess
from easygui_qt import get_color_rgb
goodbye = (""" 
███████╗███████╗███████╗    ██╗   ██╗ ██████╗ ██╗   ██╗    ███╗   ██╗███████╗██╗  ██╗████████╗    ████████╗██╗███╗   ███╗███████╗
██╔════╝██╔════╝██╔════╝    ╚██╗ ██╔╝██╔═══██╗██║   ██║    ████╗  ██║██╔════╝╚██╗██╔╝╚══██╔══╝    ╚══██╔══╝██║████╗ ████║██╔════╝
███████╗█████╗  █████╗       ╚████╔╝ ██║   ██║██║   ██║    ██╔██╗ ██║█████╗   ╚███╔╝    ██║          ██║   ██║██╔████╔██║█████╗  
╚════██║██╔══╝  ██╔══╝        ╚██╔╝  ██║   ██║██║   ██║    ██║╚██╗██║██╔══╝   ██╔██╗    ██║          ██║   ██║██║╚██╔╝██║██╔══╝  
███████║███████╗███████╗       ██║   ╚██████╔╝╚██████╔╝    ██║ ╚████║███████╗██╔╝ ██╗   ██║          ██║   ██║██║ ╚═╝ ██║███████╗
╚══════╝╚══════╝╚══════╝       ╚═╝    ╚═════╝  ╚═════╝     ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝   ╚═╝          ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝                                                                                                                                
	""")
if os.geteuid() == 0:
    try:
        print("\033[31mWARN:\033[33m program is running as sudo, please run it without sudo! Because it will not work!\033[0m")
        sleep(1)
        exit()
    except KeyboardInterrupt:
        print(f"\033[1;32;3m{goodbye}")
        sleep(0.5)
else:
    os.system("clear")

# Run the PowerShell command and capture the output
result = subprocess.run(['whoami'],
                        capture_output=True, text=True)
usr = result.stdout.strip()

thepath = f"/home/{usr}/ezpkg/packages"
temppath = f"/home/{usr}/ezpkg/temp"

def chkpath():
    # Execute the command
    return_code = os.system(f"ls {thepath}")
    
    # Extract the return code
    actual_return_code = return_code >> 8
    
    return actual_return_code
if chkpath() > 0:
	os.system("clear")
	print("\033[31mhmm.. it seems like /ezpkg is not found , lemme create it for u....\033[33m")
	os.system(f"mkdir /home/{usr}/ezpkg/ && mkdir /home/{usr}/ezpkg/temp/ && mkdir /home/{usr}/ezpkg/packages")
elif chkpath() == 0:
	os.system("clear")

chkpath()

def color():
    rgb = get_color_rgb()
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    ansi = f"\033[38;2;{r};{g};{b}m"
    return ansi
def install(dpkg):
    zip_file_path = os.path.join(temppath, f"{dpkg}.zip")
    
    # Specify the full path including the filename
    zip_file_path = os.path.join(temppath, f"{dpkg}.zip")

    try:
        # Send a GET request to the URL
        response = requests.get(f"https://ayinalienbruvinnitwenomechainsamaswaghettiliciousawesomesauce.online/{dpkg}.zip", stream=True)
        response.raise_for_status()  # Check if the request was successful

        # Write the content to the specified path
        with open(zip_file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):  # Download in chunks
                if chunk:
                    file.write(chunk)
        print(f"File downloaded successfully to {zip_file_path}, now installing...")
    except requests.RequestException as e:
        print(f"Error downloading file: {e}")

    # Extract the zip file
    try:
        with ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(thepath)
        print("Package downloaded and extracted successfully")
    except Exception as e:
        print(f"Error extracting the zip file: {e}")
        return

    # Remove the zip file
    try:
        os.remove(zip_file_path)
        print("Zip file removed successfully")
    except Exception as e:
        print(f"Error removing the zip file: {e}")
def upload():
	url = 'https://fastink.alwaysdata.net/upload'
	print("If you want to upload Python file, please put it inside a folder named after the package. The folder and zip file should both have the same name as the package for installation using install <pkg>")
	file_path = input("Enter package path (make sure to compress folder before upload) (only zip file's are allowed): ")
	print(file_path)
	with open(file_path, 'rb') as file:
			files = {'file': file}
			response = requests.post(url, files=files)
			print(response.json())

def uninstall(upkg):
    pathpkg = f"{thepath}/{upkg}"
    if os.path.exists(pathpkg) and os.path.isdir(pathpkg):
        shutil.rmtree(pathpkg)
        print(f"{upkg} has been uninstalled.")
    else:
        print(f"{upkg} not found? Maybe check {thepath}/{upkg}?")
def packageslist():
    try:
        # Get a list of all entries in the directory
        entries = os.listdir(thepath)
        # Filter out only directories
        folders = [entry for entry in entries if os.path.isdir(os.path.join(thepath, entry))]
        if folders == []:
            return "\033[1;33mYou didnt install anything?"
        return folders
    except FileNotFoundError:
        print(f"The path '{thepath}' does not exist (maybe you haven't installed anything yet....)")
    except PermissionError:
        print(f"Permission denied to access '{thepath}'.")

def update():
    print("\033[1;32;3mstill in development!")
    # TODO: make the update function work!

def help():
	print(help_list)
help_list = f""" 
\033[33m		< --- help --- >
install - install a package [\033[1;32m#ezpkg \033[0m\033[1;33m<{usr}>\033[0m ~> \033[31minstall(or download) <package>		\033[33m]

uninstall - uninstall a package [\033[1;32m#ezpkg \033[0m\033[1;33m<{usr}>\033[0m ~> \033[31muninstall(or rm or delete) <package>	\033[33m]

list - lists all packages 		[\033[1;32m#ezpkg \033[0m\033[1;33m<{usr}>\033[0m ~> \033[31mlist(or ls)	\033[33m]

update - update all packages 		[\033[1;32m#ezpkg \033[0m\033[1;33m<{usr}>\033[0m ~> \033[31mupdate	\033[33m]
colorgui - changes color (gui) [\033[1;32m#ezpkg \033[0m\033[1;33m<{usr}>\033[0m ~> \033[31mcolorgui	\033[33m]
        < --- help --- >
\033[0m
"""
color1 = "\033[1;32m"
color2 = "\033[1;33m"

print("Welcome to ezpkg cli do h (or help) for commands")
while True:
    try:    
        cmd = input(f"{color1}#ezpkg \033[0m{color2}<{usr}>\033[0m ~>")
        cmd_pro = cmd.lower()
        cmd_handle = cmd_pro.split(" ")
        
        # cmd's
        if cmd_handle[0] == "install" or cmd_handle[0] == "download":
            install(cmd_handle[1])
        elif cmd_handle[0] == "upload":
            upload()
        elif cmd_handle[0] == "list" or cmd_handle[0] == "ls":
            print(packageslist())
        elif cmd_handle[0] == "uninstall" or cmd_handle[0] == "rm" or cmd_handle[0] == "delete":
            uninstall(cmd_handle[1])
        elif cmd_handle[0] == "update" or cmd_handle[0] == "upgrade":
            update()
        elif cmd_handle[0] == "colorgui":
            print("Select `#ezpkg` color")
            color1 = color()
            print(f"Select `<{usr}>` color")
            color2 = color()
            print("\033[1;32;3mDone!\033[0m")
        elif cmd_handle[0] == "exit" or cmd_handle[0] == "break":
            print(f"\033[1;32;3m{goodbye}")
            sleep(0.5)
            break
        elif cmd_handle[0] == "h" or cmd_handle[0] == "help":
            print(help_list)       
    except KeyboardInterrupt:
        print(f"\033[1;32;3m{goodbye}")
        sleep(0.5)
        break
