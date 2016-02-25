import imaplib
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('pwmcats@gmail.com', 'pussymoneyweed')
mail.list()
# Out: list of "folders" aka labels in gmail.
mail.select("inbox") # connect to inbox.

result, data = mail.uid('search', None, "ALL") # search and return uids instead
latest_email_uid = data[0].split()[-1]
result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
raw_email = data[0][1]

import email
email_message = email.message_from_string(raw_email)
 
 # Print Message Body
for part in email_message.walk():
    # each part is a either non-multipart, or another multipart message
    # that contains further parts... Message is organized like a tree
    if part.get_content_type() == 'text/plain':
        print part.get_payload() # prints the raw text

import re
body = str(part.get_payload())        
if re.search('lightning', body):
    print "Matches"
else:
	print "These do not match"
	
