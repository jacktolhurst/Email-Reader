from imap_tools import MailBox
from tkinter import filedialog
import tkinter as tk
import os

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

def SantiseNameForFile(name:str) -> str:
    return name.replace(":", "-").replace("/", "-").replace("\\", "-")

folder = GetFolderInteractive()

messages = FindEmailWithUsername(*GetUserInformation(),depth=20)

for message in messages:
    name =  message.date_str + " " + message.from_
    print(CreateTXTFile(folder, name, message.text or message.html))