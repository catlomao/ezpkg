import os
from time import sleep
import shutil
import requests
from zipfile import ZipFile
import subprocess

# Run the PowerShell command and capture the output
result = subprocess.run(['powershell', '-Command', '(Get-WmiObject -Class Win32_OperatingSystem).SystemDrive'],
                        capture_output=True, text=True)
maindrive = result.stdout.strip()
# Define the paths
thepath = fr"{maindrive}\ezpkg\packages"
temppath = fr"{maindrive}\ezpkg\temp"


def chkpath():
    # Execute the command
    return_code = os.system(f"dir {thepath}")
    
    # Extract the return code
    actual_return_code = return_code >> 8
    
    return actual_return_code
if chkpath() > 0:
    os.system("cls")
    dirs =  [
    f'{maindrive}\\ezpkg',
    f'{thepath}',
    f'{temppath}',
   ]

    # Create each directory
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)
elif chkpath() == 0:
    os.system("cls")

chkpath()

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
    print("If you want to upload Python code, please put it inside a folder named after the package. The folder and zip file should both have the same name as the package for installation using install <pkg>")
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
        return folders
    except FileNotFoundError:
        print(f"The path '{thepath}' does not exist (maybe you haven't installed anything yet....)")
    except PermissionError:
        print(f"Permission denied to access '{thepath}'.")

def help():
    print(help_list)
help_list = """ 
\033[33m        < --- help --- >
install - install a package [\033[31m%> install <package>       \033[33m]

uninstall - uninstall a package [\033[31m%> uninstall <package> \033[33m]

list - lists all packages       [\033[31m%> list    \033[33m]
        < --- help --- >
\033[0m
"""
goodbye = (""" 
███████╗███████╗███████╗    ██╗   ██╗ ██████╗ ██╗   ██╗    ███╗   ██╗███████╗██╗  ██╗████████╗    ████████╗██╗███╗   ███╗███████╗
██╔════╝██╔════╝██╔════╝    ╚██╗ ██╔╝██╔═══██╗██║   ██║    ████╗  ██║██╔════╝╚██╗██╔╝╚══██╔══╝    ╚══██╔══╝██║████╗ ████║██╔════╝
███████╗█████╗  █████╗       ╚████╔╝ ██║   ██║██║   ██║    ██╔██╗ ██║█████╗   ╚███╔╝    ██║          ██║   ██║██╔████╔██║█████╗  
╚════██║██╔══╝  ██╔══╝        ╚██╔╝  ██║   ██║██║   ██║    ██║╚██╗██║██╔══╝   ██╔██╗    ██║          ██║   ██║██║╚██╔╝██║██╔══╝  
███████║███████╗███████╗       ██║   ╚██████╔╝╚██████╔╝    ██║ ╚████║███████╗██╔╝ ██╗   ██║          ██║   ██║██║ ╚═╝ ██║███████╗
╚══════╝╚══════╝╚══════╝       ╚═╝    ╚═════╝  ╚═════╝     ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝   ╚═╝          ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝                                                                                                                                
    """)
while True:
    try:    
        print("Welcome to ezpkg cli do h (or help) for commands")
        cmd = input("ezpkg !> ")
        cmd_pro = cmd.lower()
        cmd_handle = cmd_pro.split(" ")
        # cmd's
        if cmd_handle[0] == "install":
            install(cmd_handle[1])
        elif cmd_handle[0] == "upload":
            upload()
        elif cmd_handle[0] == "list":
            print(packageslist())
        elif cmd_handle[0] == "uninstall":
            uninstall(cmd_handle[1])
        elif cmd_handle[0] == "exit":
            print(f"\033[1;32;3m{goodbye}")
            sleep(0.5)
            break
        elif cmd_handle[0] == "h" or "help":
            print(help_list)
    except KeyboardInterrupt:
        print(f"\033[1;32;3m{goodbye}")
        sleep(0.5)
        break