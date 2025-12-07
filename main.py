from tkinter import filedialog
import tkinter as tk
import json
import subprocess
import sys
import os
from swinlnk.swinlnk import SWinLnk

def CreateExe(scriptPath: str, outputName: str) -> str:
    try:
        import PyInstaller
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                            stdout=subprocess.DEVNULL, 
                            stderr=subprocess.DEVNULL)
    
    exe_name = outputName if outputName else os.path.splitext(os.path.basename(scriptPath))[0]
    exe_path = os.path.abspath(f"./{exe_name}.exe")
    cmd = [sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole"]
    cmd.extend(["--name", exe_name])
    cmd.extend(["--distpath", "."])
    cmd.extend(["--workpath", "./build"])
    cmd.extend(["--specpath", "."])
    cmd.append(scriptPath)
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    return exe_path

def CreateShortcut(targetPath: str, shortcutPath: str) -> str:
    swl = SWinLnk()

    if not shortcutPath.lower().endswith(".lnk"):
        base = os.path.basename(targetPath)
        shortcutPath = os.path.join(shortcutPath, f"{base}.lnk")

    swl.create_lnk(targetPath, shortcutPath)

    return os.path.abspath(shortcutPath)

def GetFolderInteractive() -> str:
    root = tk.Tk()
    root.withdraw()
    
    folder_path = filedialog.askdirectory(title="Select a folder for files to be saved")
    
    root.destroy() 
    return folder_path

def GetUserInformation() -> tuple[str, str, str]:
    username = input("username: ")
    
    passcode = input("2FA Code: ")
    
    checkUserName = input("Username to check: ")
    
    return username, passcode, checkUserName

def Startup():
    folder = GetFolderInteractive()

    userInformation = GetUserInformation()
    
    with open("data.json", 'w') as file:

        saveData = {
            "Folder" : folder,
            "Username" : userInformation[0],
            "Passcode" : userInformation[1],
            "CheckUsername" : userInformation[2],
            "LastCheckedEmailUid" : "None"
        }

        json.dump(saveData, file, indent=4)
    
    exePath = CreateExe("CheckEmail.py", "Email Checker")
    startupFolder = os.path.join(
        os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup"
    )

    CreateShortcut(exePath, startupFolder)

if __name__ == "__main__":
    Startup()