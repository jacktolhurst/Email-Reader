from imap_tools import MailBox
from winotify import Notification, audio
import imap_tools
import json
import os
import sys

def GetResourcePath(relativePath:str):
    basePath = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(basePath, relativePath)

def GetElapsedEmails(username:str, passcode:str, lastCheckedEmailUid:str) -> list[imap_tools.message.MailMessage]:
    elapsedEmails = []
    
    with MailBox('imap.gmail.com').login(username, passcode) as mailbox:
        for message in mailbox.fetch(reverse=True, limit=None):
            if message.uid == lastCheckedEmailUid:
                break
            else:
                elapsedEmails.append(message)
    
    return elapsedEmails

def SantiseNameForFile(name:str) -> str:
    return name.replace(":", "-").replace("/", "-").replace("\\", "-")

def CreateTXTFile(location:str, name:str, text:str) -> str:
    try:
        fileLocation = os.path.join(location, SantiseNameForFile(name) + ".txt")
        
        if not os.path.exists(fileLocation):
            with open(fileLocation, "w", encoding="utf-8") as newFile:
                newFile.write(text)
            return fileLocation  
        else:
            return None
    except:
        return None

def CreateBinaryFile(location:str, name:str, data:bytes, type:str) -> str:
    try:
        fileLocation = os.path.join(location, SantiseNameForFile(name) + "." + type)
        
        if not os.path.exists(fileLocation):
            with open(fileLocation, 'wb') as newFile:
                newFile.write(data)
            return fileLocation  
        else:
            return None
    except:
        return None

def InstallEmailWithGivenUsername(emails:list[imap_tools.message.MailMessage], checkUsername:str, folder:str) -> list[imap_tools.message.MailMessage]:
    downloadedEmails = []
    
    for email in emails:
        if  email.from_ == checkUsername:
            downloadedEmails.append(email)
            
            name =  email.date_str + " " + email.from_
            
            CreateTXTFile(folder, name, email.text or email.html)

            for attribute in email.attachments:
                type = os.path.splitext(attribute.filename)[1].lstrip('.') 
                CreateBinaryFile(folder, name + " " + type, attribute.payload, type)
    
    return downloadedEmails

def CreateNotification(notificationName:str, notificationBody:str, duration:int, *, iconPath:str = None):
    toast = Notification(
        app_id="Email Checker",
        title=notificationName,
        msg=notificationBody,
        duration="short" if duration <= 10 else "long"
    )
    
    if iconPath:
        toast.set_icon(iconPath)
    
    toast.show()

if __name__ == "__main__":
    
    with open(GetResourcePath("data.json"), 'r') as file:
        data = json.load(file)
        
        elapsedEmails = GetElapsedEmails(data["Username"], data["Passcode"], data["LastCheckedEmailUid"])
        
        if elapsedEmails:
            downloadedEmails = InstallEmailWithGivenUsername(elapsedEmails, data["CheckUsername"], data["Folder"])
            
            saveData = {
                "Folder" : data["Folder"],
                "Username" : data["Username"],
                "Passcode" : data["Passcode"],
                "CheckUsername" : data["CheckUsername"],
                "LastCheckedEmailUid" : elapsedEmails[0].uid
            }
            with open(GetResourcePath("data.json"), 'w') as newFile:
                json.dump(saveData, newFile, indent=4)
                
            CreateNotification("Some of " + data["CheckUsername"] + "'s emails have been downloaded", "Downloaded " + str(len(downloadedEmails)) + " emails into " + data["Folder"], 20)
        
        else:
            CreateNotification("No new " + data["CheckUsername"] + " emails where found", " ", 20)