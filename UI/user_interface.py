import imaplib
import email
import re
import urllib2
import json
import sys
from PyQt4 import QtGui, QtCore

#Global Variables
global light_selection
light_selection = "No Light"
global aural_selection
aural_selection = "No Alert"
global hours
hours = "0"
global minutes
minutes = "0"
global current_light
current_light = "No Light"
global current_aural
current_aural = "No Alert"


#Temporary send function to print message
def send(logic_code):
	print logic_code
	
#Gather Weather Data From WunderGround and return wind speed
def gather_wind():
	f = urllib2.urlopen('http://api.wunderground.com/api/4bb2e676301d811b/conditions/q/WA/EVERETT.json')
	json_string = f.read()
	parsed_json = json.loads(json_string)
	wind_speed = parsed_json['current_observation']['wind_mph']
	return float(wind_speed)
	
#Gather Weather Data From WunderGround and return Temp in F
def gather_temp():
	f = urllib2.urlopen('http://api.wunderground.com/api/4bb2e676301d811b/conditions/q/WA/EVERETT.json')
	json_string = f.read()
	parsed_json = json.loads(json_string)
	temp_f = parsed_json['current_observation']['temp_f']
	return str(temp_f)

#Gather Weather Data From WunderGround and return wind direction
def gather_direction():
	f = urllib2.urlopen('http://api.wunderground.com/api/4bb2e676301d811b/conditions/q/WA/EVERETT.json')
	json_string = f.read()
	parsed_json = json.loads(json_string)
	direction = parsed_json['current_observation']['wind_dir']
	return str(direction)

#This function checks for the most recent email in the inbox and 
#Turns on the corresponding light and siren. 
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
        
        self.activate_button = QtGui.QPushButton('Send Alert', self)
        self.activate_button.setToolTip('This activates the set alerts')
        self.activate_button.resize(self.activate_button.sizeHint())
        self.activate_button.move(125, 225)
        self.activate_button.clicked.connect(self.clicked_button)
        
        #Visual Dropdown Menu
        self.lbl = QtGui.QLabel("Visual Alerts", self)
        self.visual = QtGui.QComboBox(self)
        self.visual.setToolTip('Select the visual alert you want to activate')
        self.visual.addItem("No Light")
        self.visual.addItem("Red")
        self.visual.addItem("Yellow")
        self.visual.addItem("Blue")
        
        self.visual.move(50, 75)
        self.lbl.move(52, 55)
        self.visual.activated[str].connect(self.visualchanged)
        
        #Aural Dropdown Menu
        self.lbl = QtGui.QLabel("Aural Alerts", self)
        self.aural = QtGui.QComboBox(self)
        self.aural.setToolTip('Select the aural alert you want to activate')
        self.aural.addItem("No Alert")
        self.aural.addItem("Lightning1")
        self.aural.addItem("Lightning2")  
        self.aural.addItem("Lightning3")  
        self.aural.addItem("Wind1")  
        self.aural.addItem("Wind2")  
        self.aural.addItem("Wind3")  
        self.aural.addItem("Shelter")  
        self.aural.addItem("Fuck")  
        self.aural.addItem("Shit")
        
        self.aural.move(200, 75)
        self.lbl.move(202, 55)
        self.aural.activated[str].connect(self.auralchanged)
        
        #Set Duration
        #Hour Dropdown Menu
        self.lbl = QtGui.QLabel("Visual Alerts", self)
        self.hour = QtGui.QComboBox(self)
        self.hour.setToolTip('Select the number of hours for the alert')
        self.hour.addItem("Hours")
        self.hour.addItem("0")
        self.hour.addItem("1")
        self.hour.addItem("2")
        self.hour.addItem("3")
        self.hour.addItem("4")
        self.hour.addItem("5")
        self.hour.addItem("6")
        self.hour.addItem("7")
        self.hour.addItem("8")
        self.hour.addItem("9")
        self.hour.addItem("10")
        self.hour.addItem("11")
        self.hour.addItem("12")
        self.hour.addItem("13")
        self.hour.addItem("14")
        self.hour.addItem("15")
        self.hour.addItem("16")
        self.hour.addItem("17")
        self.hour.addItem("18")
        self.hour.addItem("19")
        self.hour.addItem("20")
        self.hour.addItem("21")
        self.hour.addItem("22")
        self.hour.addItem("23")
        self.hour.addItem("24")
        
        self.hour.move(50, 175)
        self.lbl.move(52, 155)
        self.hour.activated[str].connect(self.hourchanged)
        
        #Aural Dropdown Menu
        self.lbl = QtGui.QLabel("Aural Alerts", self)
        self.minute = QtGui.QComboBox(self)
        self.minute.setToolTip('Select the number of minutes for the alert')
        self.minute.addItem("Minutes")
        self.minute.addItem("0")
        self.minute.addItem("1")
        self.minute.addItem("2")
        self.minute.addItem("3")
        self.minute.addItem("4")
        self.minute.addItem("5")
        self.minute.addItem("6")
        self.minute.addItem("7")
        self.minute.addItem("8")
        self.minute.addItem("9")
        self.minute.addItem("10")
        self.minute.addItem("11")
        self.minute.addItem("12")
        self.minute.addItem("13")
        self.minute.addItem("14")
        self.minute.addItem("15")
        self.minute.addItem("16")
        self.minute.addItem("17")
        self.minute.addItem("18")
        self.minute.addItem("19")
        self.minute.addItem("20")
        self.minute.addItem("21")
        self.minute.addItem("22")
        self.minute.addItem("23")
        self.minute.addItem("24")
        self.minute.addItem("25")
        self.minute.addItem("26")
        self.minute.addItem("27")
        self.minute.addItem("28")
        self.minute.addItem("29")
        self.minute.addItem("30")
        self.minute.addItem("31")
        self.minute.addItem("32")
        self.minute.addItem("33")
        self.minute.addItem("34")
        self.minute.addItem("35")
        self.minute.addItem("36")
        self.minute.addItem("37")
        self.minute.addItem("38")
        self.minute.addItem("39")
        self.minute.addItem("40")
        self.minute.addItem("41")
        self.minute.addItem("42")
        self.minute.addItem("43")
        self.minute.addItem("44")
        self.minute.addItem("45")
        self.minute.addItem("46")
        self.minute.addItem("47")
        self.minute.addItem("48")
        self.minute.addItem("49")
        self.minute.addItem("50")
        self.minute.addItem("51")
        self.minute.addItem("52")
        self.minute.addItem("53")
        self.minute.addItem("54")
        self.minute.addItem("55")
        self.minute.addItem("56")
        self.minute.addItem("57")
        self.minute.addItem("58")
        self.minute.addItem("59")
        self.minute.addItem("60")
        self.minute.move(200, 175)
        
        self.lbl.move(202, 155) 
        self.minute.activated[str].connect(self.minutechanged) 
        
        #Temp Display
        temp = gather_temp()
        self.temp_lbl = QtGui.QLabel("Current Temperature:", self)
        self.temp_lbl.move(0, 400)
        
        self.temperature = QtGui.QLabel("%s\xb0F" %temp, self)
        newfont = QtGui.QFont("Times", 14, QtGui.QFont.Bold)
        self.temperature.setFont(newfont)
        self.temperature.move(147, 398)
        
        #Aural Display
        self.aural_lbl = QtGui.QLabel("Aural:", self)
        self.aural_lbl.move(0, 375)
        
        self.aural_alert = QtGui.QLabel("No Alert", self)
        newfont = QtGui.QFont("Times", 14, QtGui.QFont.Bold)
        self.aural_alert.setFont(newfont)
        self.aural_alert.move(45, 372)
        
        
        #Wind Speed Display
        wind = gather_wind()
        direction = gather_direction()
        self.wind_lbl = QtGui.QLabel("Current Wind Speed:", self)
        self.wind_lbl.move(0, 430)
        
        self.wind_speed = QtGui.QLabel("%s mph %s" %(wind, direction), self)
        newfont = QtGui.QFont("Times", 14, QtGui.QFont.Bold)
        self.wind_speed.setFont(newfont)
        self.wind_speed.move(140, 426)       
        
        #Snowfall Height
        self.snow_lbl = QtGui.QLabel("Current Snow Pack:", self)
        self.snow_lbl.move(0, 450)
        
        self.snow = QtGui.QLabel("0 in", self)
        newfont = QtGui.QFont("Times", 14, QtGui.QFont.Bold)
        self.snow.setFont(newfont)
        self.snow.move(132, 447)  
        
        #Labels
        #Manual Input
        self.manual_lbl = QtGui.QLabel("Manual Inputs", self)
        newfont = QtGui.QFont("Times", 30, QtGui.QFont.Bold) 
        self.manual_lbl.setFont(newfont)
        
        #Current Conditions
        self.current_lbl = QtGui.QLabel("Current Conditions", self)
        newfont = QtGui.QFont("Times", 30, QtGui.QFont.Bold)
        self.current_lbl.setFont(newfont)
        self.current_lbl.move(0, 300)
        
        #Lights
        self.light_lbl = QtGui.QLabel("Light:", self)
        self.light_lbl.move(0, 350)
        
        #Duration
        self.duration_lbl = QtGui.QLabel("Duration", self)
        self.duration_lbl.move(150, 125)
        newfont = QtGui.QFont("Times", 14, QtGui.QFont.Bold)
        self.duration_lbl.setFont(newfont)
        
        #Communication Status
        self.comm_lbl = QtGui.QLabel("Communication Status:", self)
        self.comm_lbl.move(0, 475)
        
        #Light Color
        self.light_col = QtGui.QColor(0, 0, 255)
        self.square = QtGui.QFrame(self)
        self.square.setGeometry(43, 350, 50, 15)
        self.square.setStyleSheet("QWidget { background-color: %s }" %  
        self.light_col.name())
        
        #Communication Status Indicator
        self.comm_col = QtGui.QColor(0, 255, 0)
        self.square = QtGui.QFrame(self)
        self.square.setGeometry(155, 477, 50, 15)
        self.square.setStyleSheet("QWidget { background-color: %s }" %  
        self.comm_col.name())
        
        #Update Timer
        self.my_timer = QtCore.QTimer()
        self.my_timer.timeout.connect(self.update_gui)
        self.my_timer.start(6000) #6 sec interval
        
    	#Activate Window
        self.setGeometry(150, 290, 400, 600)
        self.setWindowTitle('Severe Weather Warning System User Interface')
        self.show()
        self.update_gui()
        
    def update_gui(self):
    	global current_light
    	global current_aural
    	print self.aural_alert
    	self.aural_alert = QtGui.QLabel("%s" %current_aural, self)
    	
    	
    def clicked_button(self):
    	global current_light
    	global current_aural
        if light_selection == "No Light":
			current_light = "No Light"
			if aural_selection == "No Alert":
				send("0a0")
				current_aural = "No Alert"
			elif aural_selection == "Lightning1":
				send("0b0")
				current_aural = "Lightning1"
			elif aural_selection == "Lightning2":
				send("0c0")
				current_aural = "Lightning2"
			elif aural_selection == "Lightning3":
				send("0d0")
				current_aural = "Lightning3"
			elif aural_selection == "Wind1":
				send("0e0")
				current_aural = "Wind1"
			elif aural_selection == "Wind2":
				send("0f0")
				current_aural = "Wind2"
			elif aural_selection == "Wind3":
				send("0g0")
				current_aural = "Wind3"
			elif aural_selection == "Shelter":
				send("0h0")
				current_aural = "Shelter"
			elif aural_selection == "Fuck":
				send("0i0")
				current_aural = "Fuck"
			elif aural_selection == "Shit":
				send("0j0")
				current_aural = "Shit"
        elif light_selection == "Red":
			current_light = "Red"
			if aural_selection == "No Alert":
				send("Ra0")
				current_aural = "No Alert"
			elif aural_selection == "Lightning1":
				send("Rb0")
				current_aural = "Lightning1"
			elif aural_selection == "Lightning2":
				send("Rc0")
				current_aural = "Lightning2"
			elif aural_selection == "Lightning3":
				send("Rd0")
				current_aural = "Lightning3"
			elif aural_selection == "Wind1":
				send("Re0")
				current_aural = "Wind1"
			elif aural_selection == "Wind2":
				send("Rf0")
				current_aural = "Wind2"
			elif aural_selection == "Wind3":
				send("Rg0")
				current_aural = "Wind3"
			elif aural_selection == "Shelter":
				send("Rh0")
				current_aural = "Shelter"
			elif aural_selection == "Fuck":
				send("Ri0")
				current_aural = "Fuck"
			elif aural_selection == "Shit":
				send("Rj0")
				current_aural = "Shit"
        elif light_selection == "Yellow":
			current_light = "Yellow"
			if aural_selection == "No Alert":
				send("Ya0")
				current_aural = "No Alert"
			elif aural_selection == "Lightning1":
				send("Yb0")
				current_aural = "Lightning1"
			elif aural_selection == "Lightning2":
				send("Yc0")
				current_aural = "Lightning2"
			elif aural_selection == "Lightning3":
				send("Yd0")
				current_aural = "Lightning3"
			elif aural_selection == "Wind1":
				send("Ye0")
				current_aural = "Wind1"
			elif aural_selection == "Wind2":
				send("Yf0")
				current_aural = "Wind2"
			elif aural_selection == "Wind3":
				send("Yg0")
				current_aural = "Wind3"
			elif aural_selection == "Shelter":
				send("Yh0")
				current_aural = "Shelter"
			elif aural_selection == "Fuck":
				send("Yi0")
				current_aural = "Fuck"
			elif aural_selection == "Shit":
				send("Yj0")
				current_aural = "Shit"
        elif light_selection == "Blue":
			current_light = "Blue"
			if aural_selection == "No Alert":
				send("Ba0")
				current_aural = "No Alert"
			elif aural_selection == "Lightning1":
				send("Bb0")
				current_aural = "Lightning1"
			elif aural_selection == "Lightning2":
				send("Bc0")
				current_aural = "Lightning2"
			elif aural_selection == "Lightning3":
				send("Bd0")
				current_aural = "Lightning3"
			elif aural_selection == "Wind1":
				send("Be0")
				current_aural = "Wind1"
			elif aural_selection == "Wind2":
				send("Bf0")
				current_aural = "Wind2"
			elif aural_selection == "Wind3":
				send("Bg0")
				current_aural = "Wind3"
			elif aural_selection == "Shelter":
				send("Bh0")
				current_aural = "Shelter"
			elif aural_selection == "Fuck":
				send("Bi0")
				current_aural = "Fuck"
			elif aural_selection == "Shit":
				send("Bj0")
				current_aural = "Shit"
        global minutes
        if (int(minutes) > 0) or (int(hours) > 0):
			self.timer = QtCore.QTimer()
			self.timer.singleShot((int(hours)*3600000) + (int(minutes)*6000), self.off_signal)
			
    def off_signal(self):
		send("0a0")
				
    def visualchanged(self):
		global visual_selection
		visual_selection = str(self.visual.currentText())
	
    def auralchanged(self):
		global aural_selection
		aural_selection = str(self.aural.currentText())
		
    def hourchanged(self):
    	global hours
    	hours = str(self.hour.currentText())
    	
    def minutechanged(self):
    	global minutes
    	minutes = str(self.minute.currentText())
	
#main Function
message = 'initial'    
def main():
	app = QtGui.QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()