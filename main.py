from imap_tools import MailBox
from tkinter import filedialog
import tkinter as tk

def GetFolderInteractive() -> str:
    root = tk.Tk()
    root.withdraw()
    
    folder_path = filedialog.askdirectory(title="Select a folder for files to be saved")
    
    root.destroy() 
    return folder_path

def FindEmailWithUsername(username:str, passcode:str, checkUserName:str, depth:int=None, reverse:bool=True):
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

folder = GetFolderInteractive()

print(FindEmailWithUsername(*GetUserInformation()))

