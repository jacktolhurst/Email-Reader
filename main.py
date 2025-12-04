from imap_tools import MailBox
from tkinter import filedialog
import tkinter as tk
import os
import json
import html2text

def GetFolderInteractive() -> str:
    root = tk.Tk()
    root.withdraw()
    
    folder_path = filedialog.askdirectory(title="Select a folder for files to be saved")
    
    root.destroy() 
    return folder_path

def FindEmailWithUsername(username:str, passcode:str, checkUserName:str, *, depth:int=None, reverse:bool=True):
    foundMessages = []
    
    with MailBox('imap.gmail.com').login(username, passcode) as mailbox:
        for msg in mailbox.fetch(reverse=reverse, limit=depth):
            if  msg.from_ == checkUserName:
                foundMessages.append(msg)
    
    return foundMessages

def GetUserInformation() -> tuple[str, str, str]:
    username = input("username: ")
    
    passcode = input("2FA Code: ")
    
    checkUserName = input("Username to check: ")
    
    return username, passcode, checkUserName

def CreateTXTFile(location:str, name:str, text:str) -> str:
    try:
        fileLocation = os.path.join(location, SantiseNameForFile(name) + ".txt")
        
        if not os.path.exists(fileLocation):
            with open(fileLocation, "w", encoding="utf-8") as newFile:
                newFile.write(text)
            return fileLocation  
        else:
            print("A file by that name already exists")
            return None
    except Exception as err:
        print(err)
        return None

def AddToStartup():
    startup_folder = os.path.join(
        os.getenv('APPDATA'), 
        'Microsoft\\Windows\\Start Menu\\Programs\\Startup'
    )
    
    script_path = os.path.abspath(__file__)
    bat_path = os.path.join(startup_folder, "email_checker.bat")
    
    with open(bat_path, 'w') as f:
        f.write(f'@echo off\npython "{script_path}"\n')

def SantiseNameForFile(name:str) -> str:
    return name.replace(":", "-").replace("/", "-").replace("\\", "-")

def HTMLToText(html:str) -> str:
    return html2text.html2text(html)


def Startup():
    folder = GetFolderInteractive()

    userInformation = GetUserInformation()
    
    AddToStartup()
    
    with open("data.json", 'w') as file:

        saveData = {
            "Started" : True,
            "Folder" : folder,
            "Username" : userInformation[0],
            "Passcode" : userInformation[1],
            "CheckUsername" : userInformation[2]
        }

        json.dump(saveData, file, indent=4)

def Checkmessages():
    with open("data.json", 'r') as file:
        data = json.load(file)
        
        folder = data["Folder"]
        username = data["Username"]
        passcode = data["Passcode"]
        checkUsername = data["CheckUsername"]
    
    messages = FindEmailWithUsername(username, passcode, checkUsername,depth=20)

    for message in messages:
        name =  message.date_str + " " + message.from_
        print(CreateTXTFile(folder, name, message.text or HTMLToText(message.html)))

if __name__ == "__main__":
    if not os.path.exists("data.json"):
        Startup()
    
    Checkmessages()