from imap_tools import MailBox

def FindEmailWithUsername(username:str, passcode:str, checkUserName:str, depth:int=None, reverse:bool=True):
    with MailBox('imap.gmail.com').login(username, passcode) as mailbox:
        for msg in mailbox.fetch(reverse=reverse, limit=depth):
            if  msg.from_ == checkUserName:
                print(msg.from_, msg.subject)

def GetUserInformation() -> tuple[str, str, str]:
    username = input("username: ")
    
    passcode = input("2FA Code: ")
    
    checkUserName = input("Username to check: ")
    
    return username, passcode, checkUserName

FindEmailWithUsername(*GetUserInformation())

