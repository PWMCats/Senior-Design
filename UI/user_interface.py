import imaplib
import email
import re
import sys
from PyQt4 import QtGui, QtCore

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

#GUI window formatting
class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        #Button
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        
        activate = QtGui.QPushButton('Send Alert', self)
        activate.setToolTip('This activates the set alerts')
        activate.resize(activate.sizeHint())
        activate.move(125, 225)
        
        #Visual Dropdown Menu
        self.lbl = QtGui.QLabel("Visual Alerts", self)
        visual = QtGui.QComboBox(self)
        visual.setToolTip('Select the visual alert you want to activate')
        visual.addItem("No Light")
        visual.addItem("Red")
        visual.addItem("Yellow")
        visual.addItem("Blue")
        
        visual.move(50, 75)
        self.lbl.move(52, 55)
        
        #Aural Dropdown Menu
        self.lbl = QtGui.QLabel("Aural Alerts", self)
        aural = QtGui.QComboBox(self)
        aural.setToolTip('Select the aural alert you want to activate')
        aural.addItem("No Alert")
        aural.addItem("Lightning1")
        aural.addItem("Lightning2")  
        aural.addItem("Lightning3")  
        aural.addItem("Wind1")  
        aural.addItem("Wind2")  
        aural.addItem("Wind3")  
        aural.addItem("Shelter")  
        aural.addItem("Fuck")  
        aural.addItem("Shit")
        
        aural.move(200, 75)
        self.lbl.move(202, 55)
        
        #Set Duration
        #Hour Dropdown Menu
        self.lbl = QtGui.QLabel("Visual Alerts", self)
        hour = QtGui.QComboBox(self)
        hour.setToolTip('Select the number of hours for the alert')
        hour.addItem("Hours")
        hour.addItem("0")
        hour.addItem("1")
        hour.addItem("2")
        hour.addItem("3")
        hour.addItem("4")
        hour.addItem("5")
        hour.addItem("6")
        hour.addItem("7")
        hour.addItem("8")
        hour.addItem("9")
        hour.addItem("10")
        hour.addItem("11")
        hour.addItem("12")
        
        hour.move(50, 175)
        self.lbl.move(52, 155)
        
        #Aural Dropdown Menu
        self.lbl = QtGui.QLabel("Aural Alerts", self)
        minute = QtGui.QComboBox(self)
        minute.setToolTip('Select the number of minutes for the alert')
        minute.addItem("Minutes")
        minute.addItem("0")
        minute.addItem("1")
        minute.addItem("2")
        minute.addItem("3")
        minute.addItem("4")
        minute.addItem("5")
        minute.addItem("6")
        minute.addItem("7")
        minute.addItem("8")
        minute.addItem("9")
        minute.addItem("10")
        minute.addItem("11")
        minute.addItem("12")
        minute.addItem("13")
        minute.addItem("14")
        minute.addItem("15")
        minute.addItem("16")
        minute.addItem("17")
        minute.addItem("18")
        minute.addItem("19")
        minute.addItem("20")
        minute.addItem("21")
        minute.addItem("22")
        minute.addItem("23")
        minute.addItem("24")
        minute.addItem("25")
        minute.addItem("26")
        minute.addItem("27")
        minute.addItem("28")
        minute.addItem("29")
        minute.addItem("30")
        minute.addItem("31")
        minute.addItem("32")
        minute.addItem("33")
        minute.addItem("34")
        minute.addItem("35")
        minute.addItem("36")
        minute.addItem("37")
        minute.addItem("38")
        minute.addItem("39")
        minute.addItem("40")
        minute.addItem("41")
        minute.addItem("42")
        minute.addItem("43")
        minute.addItem("44")
        minute.addItem("45")
        minute.addItem("46")
        minute.addItem("47")
        minute.addItem("48")
        minute.addItem("49")
        minute.addItem("50")
        minute.addItem("51")
        minute.addItem("52")
        minute.addItem("53")
        minute.addItem("54")
        minute.addItem("55")
        minute.addItem("56")
        minute.addItem("57")
        minute.addItem("58")
        minute.addItem("59")
        minute.addItem("60")
        minute.move(200, 175)
        self.lbl.move(202, 155)  
        
        #Temp Display
        self.lbl = QtGui.QLabel("Current Temperature:", self)
        self.lbl.move(0, 405)
        temp = QtGui.QLCDNumber(self)
        temp.move(125, 400)
        
        #Wind Speed Display
        wind = QtGui.QLCDNumber(self)
        self.lbl = QtGui.QLabel("Current Wind Speed:", self)
        self.lbl.move(0, 430)
        wind.move(125, 425)
        
        #Snowfall Height
        snow = QtGui.QLCDNumber(self)
        self.lbl = QtGui.QLabel("Current Snow Pack:", self)
        self.lbl.move(0, 455)
        snow.move(125, 450)
        
        #Labels
        #Manual Input
        self.lbl = QtGui.QLabel("Manual Inputs", self)
        newfont = QtGui.QFont("Times", 30, QtGui.QFont.Bold) 
        self.lbl.setFont(newfont)
        
        #Current Conditions
        self.lbl = QtGui.QLabel("Current Conditions", self)
        newfont = QtGui.QFont("Times", 30, QtGui.QFont.Bold)
        self.lbl.setFont(newfont)
        self.lbl.move(0, 300)
        
        #Lights
        self.lbl = QtGui.QLabel("Light:", self)
        self.lbl.move(0, 350)
        
        #Aural
        self.lbl = QtGui.QLabel("Aural:", self)
        self.lbl.move(0, 375)
        
        #Duration
        self.lbl = QtGui.QLabel("Duration", self)
        self.lbl.move(150, 125)
        newfont = QtGui.QFont("Times", 14, QtGui.QFont.Bold)
        self.lbl.setFont(newfont)
        
        #Communication Status
        self.lbl = QtGui.QLabel("Communication Status:", self)
        self.lbl.move(0, 475)
        
        #Light Color
        self.col = QtGui.QColor(0, 0, 255)
        self.square = QtGui.QFrame(self)
        self.square.setGeometry(35, 350, 50, 15)
        self.square.setStyleSheet("QWidget { background-color: %s }" %  
        self.col.name())
        
        #Communication Status
        self.col = QtGui.QColor(0, 255, 0)
        self.square = QtGui.QFrame(self)
        self.square.setGeometry(140, 475, 50, 15)
        self.square.setStyleSheet("QWidget { background-color: %s }" %  
        self.col.name())
                
    	#Activate Window
        self.setGeometry(150, 290, 400, 600)
        self.setWindowTitle('Severe Weather Warning System User Interface')
        self.show()
        
        
#Set up the window with all of the widgets
def GUI_window():
	app = QtGui.QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())

    
#main Function
message = 'initial'
while 1:
	#previous_message = message
	#message = handle_email(previous_message)
	GUI_window()
	
