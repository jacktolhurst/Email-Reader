from imap_tools import MailBox

username = input("username: ")
password = input("2FA Code: ")

checkUserName = input("Username to check: ")

depth = int(input("Email depth: "))


# Get date, subject and body len of all emails from INBOX folder
with MailBox('imap.gmail.com').login(username, password) as mailbox:
    
    for msg in mailbox.fetch(reverse=True, limit=depth):
        if  msg.from_ == checkUserName:
            print(msg.from_, msg.subject)