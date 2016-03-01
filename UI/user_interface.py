import imaplib
import email
import re
import urllib2
import json
import sys
from PyQt4 import QtGui, QtCore

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
        
        activate = QtGui.QPushButton('Send Alert', self)
        activate.setToolTip('This activates the set alerts')
        activate.resize(activate.sizeHint())
        activate.move(125, 225)
        activate.clicked.connect(self.clicked_button(light_selection, aural_selection, hours, minutes))
        #Alert Signals
        light_selection = "No Light"
        aural_selection = "No Alert"
        hours = "0"
        minutes = "0"
		
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
		self.aural.currentIndexChanged.connect(self.auralchanged)
        
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
        hour.addItem("13")
        hour.addItem("14")
        hour.addItem("15")
        hour.addItem("16")
        hour.addItem("17")
        hour.addItem("18")
        hour.addItem("19")
        hour.addItem("20")
        hour.addItem("21")
        hour.addItem("22")
        hour.addItem("23")
        hour.addItem("24")
        
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
        
    	#Activate Window
        self.setGeometry(150, 290, 400, 600)
        self.setWindowTitle('Severe Weather Warning System User Interface')
        self.show()
        
	def clicked_button(self, light_selection, aural_selection, hours, minutes):
		if light_selection == "No Light":
			if aural_selection == "No Alert"
				send("0a0")
			elif aural_selection == "Lightning1":
				send("0b0")
			elif aural_selection == "Lightning2":
				send("0c0")
			elif aural_selection == "Lightning3":
				send("0d0")
			elif aural_selection == "Wind1":
				send("0e0")
			elif aural_selection == "Wind2":
				send("0f0")
			elif aural_selection == "Wind3":
				send("0g0")
			elif aural_selection == "Shelter":
				send("0h0")
			elif aural_selection == "Fuck":
				send("0i0")
			elif aural_selection == "Shit":
				send("0j0")
		elif light_selection == "Red":
			if aural_selection == "No Alert"
				send("Ra0")
			elif aural_selection == "Lightning1":
				send("Rb0")
			elif aural_selection == "Lightning2":
				send("Rc0")
			elif aural_selection == "Lightning3":
				send("Rd0")
			elif aural_selection == "Wind1":
				send("Re0")
			elif aural_selection == "Wind2":
				send("Rf0")
			elif aural_selection == "Wind3":
				send("Rg0")
			elif aural_selection == "Shelter":
				send("Rh0")
			elif aural_selection == "Fuck":
				send("Ri0")
			elif aural_selection == "Shit":
				send("Rj0")
		elif light_selection == "Yellow":
			if aural_selection == "No Alert"
				send("Ya0")
			elif aural_selection == "Lightning1":
				send("Yb0")
			elif aural_selection == "Lightning2":
				send("Yc0")
			elif aural_selection == "Lightning3":
				send("Yd0")
			elif aural_selection == "Wind1":
				send("Ye0")
			elif aural_selection == "Wind2":
				send("Yf0")
			elif aural_selection == "Wind3":
				send("Yg0")
			elif aural_selection == "Shelter":
				send("Yh0")
			elif aural_selection == "Fuck":
				send("Yi0")
			elif aural_selection == "Shit":
				send("Yj0")
		elif light_selection == "Blue":
			if aural_selection == "No Alert"
				send("Ba0")
			elif aural_selection == "Lightning1":
				send("Bb0")
			elif aural_selection == "Lightning2":
				send("Bc0")
			elif aural_selection == "Lightning3":
				send("Bd0")
			elif aural_selection == "Wind1":
				send("Be0")
			elif aural_selection == "Wind2":
				send("Bf0")
			elif aural_selection == "Wind3":
				send("Bg0")
			elif aural_selection == "Shelter":
				send("Bh0")
			elif aural_selection == "Fuck":
				send("Bi0")
			elif aural_selection == "Shit":
				send("Bj0")
	
	def visualchanged(self):
		visual_selection = str(aural.currentText())
	
	def auralchanged(self):
		aural_selection = str(visual.currentText())
		
#main Function
message = 'initial'    
def main():
	app = QtGui.QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()