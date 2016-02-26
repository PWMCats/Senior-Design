import imaplib
import email
import re

#Temporary send function to print message
def send(logic_code):
	print logic_code

#This function checks for the most recent email in the inbox and 
#turns on the corresponding light and siren. 
def handle_email(previous_message):
	#Logs in to email account
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login('pwmcats@gmail.com', 'pussymoneyweed')
	mail.list()
	mail.select("inbox") # connect to inbox.
	
	result, data = mail.uid('search', None, "ALL") # search and return uids instead
	latest_email_uid = data[0].split()[-1]
	result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
	raw_email = data[0][1]

	email_message = email.message_from_string(raw_email)
	
	for part in email_message.walk():
		# each part is a either non-multipart, or another multipart message
		# that contains further parts... Message is organized like a tree
		if part.get_content_type() == 'text/plain':
			current_message = str(part.get_payload()) # stores current message
			#Compare current email with different messages then turn on signal
			#if no new email
			if re.search(previous_message, current_message):
				print 'stuck here'
				return current_message
			#check for lightning 1
			elif re.search('lightning1', current_message):
				send('BX0')
				return current_message
			#check for lightning 2
			elif re.search('lightning2', current_message):
				send('YX0')
				return current_message
			#check for lightning 3
			elif re.search('lightning3', current_message):
				send('RX0')
				return current_message
			#check for lightning off
			elif re.search('lightning off', current_message):
				send('OX0')
				return current_message
			#check for wind 1
			elif re.search('wind1', current_message):
				send('BX0')
				return current_message
			#check for wind 2
			elif re.search('wind2', current_message):
				send('YX0')
				return current_message
			#check for wind 3
			elif re.search('wind3', current_message):
				send('RX0')
				return current_message
			#check for wind off
			elif re.search('wind off', current_message):
				send('OX0')
				return current_message

message = 'initial'
#main Function
while 1:
	previous_message = message
	message = handle_email(previous_message)
