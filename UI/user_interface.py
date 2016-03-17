import imaplib
import email
import re
import urllib2
import json
import sys
import time
import serial
import struct
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread

#Global Variables
global light_selection
visual_selection = "No Light"
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
global current_snow
current_snow = 0
global previous_message
previous_message = "initial message"
global current_message
current_message = "no message"
global wind
global communication
communication = "Excellent"
global comm_status
comm_status = "O"
global ser
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)


#Temporary send function to print message
def send(light, track, snow):
	global ser
	global comm_status
	start=255
	
	code = ''
	
	values = (start, light, track, snow)
	
	for i in values:
		code +=struct.pack('!B',i)
	ser.write(code)
	print values
	out = ''
	#ser.fluch()
	out1 = ser.read(1)
	out2 = ser.read(1)
	comm_status = out1
	print out1, ord(out2)
	
def convert_send():
	global current_light
	global current_aural
	global current_snow
	
	#Convert current light signal to int
	if current_light == "No Light":
		light = 0
	elif current_light == "Blue":
		light = 5
	elif current_light == "Yellow":
		light = 6
	elif current_light == "Red":
		light = 7
	
	#Convert current aural signal to int	
	if current_aural == "No Alert":
		track = 0
	elif current_aural == "Lightning1":
		track = 1
	elif current_aural == "Lightning2":
		track = 2
	elif current_aural == "Lightning3":
		track = 1
	elif current_aural == "Wind1":
		track = 4
	elif current_aural == "Wind2":
		track = 5
	elif current_aural == "Wind3":
		track = 6
	
	#Send current signal
	send(light, track, current_snow)
	
		
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

#GUI window formatting
class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        
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
        
        self.aural.move(200, 75)
        self.lbl.move(202, 55)
        self.aural.activated[str].connect(self.auralchanged)
        
        #Set Duration
        #Hour Dropdown Menu
        self.lbl = QtGui.QLabel("Hours", self)
        self.hour = QtGui.QComboBox(self)
        self.hour.setToolTip('Select the number of hours for the alert')
        self.hour.addItem("Select")
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
        self.lbl = QtGui.QLabel("Minutes", self)
        self.minute = QtGui.QComboBox(self)
        self.minute.setToolTip('Select the number of minutes for the alert')
        self.minute.addItem("Select")
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
        self.aural_alert.resize(100, 20)
        
        
        #Wind Speed Display
        wind = gather_wind()
        direction = gather_direction()
        self.wind_lbl = QtGui.QLabel("Current Wind Speed:", self)
        self.wind_lbl.move(0, 430)
        
        self.wind_speed = QtGui.QLabel("%s mph %s" %(wind, direction), self)
        newfont = QtGui.QFont("Times", 14, QtGui.QFont.Bold)
        self.wind_speed.setFont(newfont)
        self.wind_speed.move(140, 426)
        self.wind_speed.resize(150, 20)
        
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
        self.comm = QtGui.QLabel("Excellent", self)
        self.comm.move(155, 475)
        
        #Light Color
        self.visual_alert = QtGui.QLabel("%s" %current_light, self)
        self.visual_alert.move(43, 350)
        newfont = QtGui.QFont("Times", 14, QtGui.QFont.Bold)
        self.visual_alert.setFont(newfont)
        
        #Timers
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_gui)
        self.update_timer.start(1000) #1 sec interval
        self.weather_timer = QtCore.QTimer()
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start(45000) #Change to 240000
                
    	#Activate Window
        self.setGeometry(150, 290, 400, 600)
        self.setWindowTitle('Severe Weather Warning System User Interface')
        self.show()
    
    def update_weather(self):
    	global wind
    	global current_snow
    	wind = gather_wind()
    	wind_dir = gather_direction()
    	temp = gather_temp()
    	if temp < 35:
    		current_snow = 0
    	else:
    		current_snow = 1
        self.wind_speed.setText("%s mph %s" %(wind, wind_dir))
        self.temperature.setText("%s\xb0F" %temp)
        print("The current wind speed is:")
        print("%s mph %s" %(wind, wind_dir))
        self.check_wind()
        
    def check_wind(self):
    	global current_light
    	global current_aural
    	global wind
    	if (wind) > 30 and (wind) <= 40:
    		current_light = "Blue"
    		current_aural = "Wind1"
    	elif (wind) > 40 and (wind) <= 50:
    		current_light = "Yellow"
    		current_aural = "Wind2"
    	elif (wind) > 50:
    		current_light = "Yellow"
    		current_aural = "Wind3"
        
    def update_gui(self):
    	global current_light
    	global current_aural
    	global comm_status
    	global communication
    	if comm_status == "O":
    		communication = "Excellent"
    	else:
    		communication = "Lost"
    	self.comm.setText(communication)
    	self.aural_alert.setText(current_aural)
    	self.visual_alert.setText(current_light)
    	
    def clicked_button(self):
    	global current_light
    	global current_aural
    	
    	current_light = visual_selection
    	current_aural = aural_selection
        
        global minutes
        global hours
        if minutes == "Select":
        	minutes = "0"
        if hours == "Select":
        	hours = "0"
        if (int(minutes) > 0) or (int(hours) > 0):
			self.timer = QtCore.QTimer()
			self.timer.singleShot((int(hours)*3600000) + (int(minutes)*60000), self.off_signal)
			
    def off_signal(self):
		global current_light
		global current_aural
		current_light = "No Light"
		current_aural = "No Alert"
				
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

class background_functions(QtCore.QThread):
    def __init__(self):
        QThread.__init__(self)
        
        #Timer to handle emails
        self.email_timer = QtCore.QTimer()
        self.email_timer.timeout.connect(self.handle_email)
        self.email_timer.start(5000)
    
    def start(self):
        QtCore.QThread.start(self)

    def run(self):
        QtCore.QThread.run(self)    
    
    def handle_email(self):
		global current_aural
		global current_light
		global previous_message
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
					previous_message = current_message
				#check for lightning 1
				elif re.search('lightning1', current_message):
					current_aural = "Lightning1"
					current_light = "Blue"
				#check for lightning 2
				elif re.search('lightning2', current_message):
					current_aural = "Lightning2"
					current_light = "Yellow"
				#check for lightning 3
				elif re.search('Type 3 Lightning', current_message):
					current_aural = "Lightning3"
					current_light = "Red"
				#check for lightning off
				elif re.search('lightning off', current_message):
					current_aural = "No Alert"
					current_light = "No Light"
				#check for wind 1
				#elif re.search('wind1', current_message):
				#check for wind 2
				#elif re.search('wind2', current_message):
				#check for wind 3
				#elif re.search('wind3', current_message):
				#check for wind off
				#elif re.search('wind off', current_message):
				
		previous_message = current_message        
    		convert_send()

        
#main Function
message = 'initial'    
def main():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    back = background_functions()
    back.start()
    sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()
