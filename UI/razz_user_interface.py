###############################################################################
# User Interface for Raspberry Pi
#
# Created By: Antonio Perez
#
# Date: 3/31/16
#
###############################################################################

#Import all libraries
import imaplib
import email
import re
import urllib2
import json
import sys
import time
import subprocess
import serial
import struct
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread
import RPi.GPIO as GPIO

#Declare all Global Variables
global light_selection                  #Current Dropdown Light Selection
global aural_selection                  #Current Dropdown Aural Selection
global hours                            #Current Dropdown Hour Selection
global minutes                          #Current Dropdown Minute Selection
global current_light                    #Current Light Selection
global current_aural                    #Current Aural Selection
global previous_light                   #Previous Light Selection
global previous_aural                   #Previous Aural Selection
global current_snow                     #Snow Detector on or off
global current_message                  #Current Email Message
global previous_message                 #Previous Email Message
global wind                             #Current Wind Speed
global communication                    #Current Communication Statues
global comm_status                      #Communication acknowledgement from uC
#global f                                #Wunderground data

#Give each global variable an initial value
visual_selection = "No Light"
aural_selection = "No Alert"
hours = "0"
minutes = "0"
current_light = "No Light"
current_aural = "No Alert"
previous_light = "none"
previous_aural = "none"
current_snow = 0
previous_message = "initial message"
current_message = "no message"
communication = "Excellent"
comm_status = "O"
#f = urllib2.urlopen('http://api.wunderground.com/api/4bb2e676301d811b/conditions/q/WA/EVERETT.json')


#Setup GPIOS
GPIO.setmode (GPIO.BCM)
GPIO.setwarnings (False)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

GPIO.output(16, True)
GPIO.output(20, True)
GPIO.output(21, True)

#Sets the hardware in the Severe Weather Warning System
def set_state():
    global current_light
    global current_aural
    global previous_light
    global previous_aural
    global current_snow
	
    #Activate Visual Alert
    if current_light != previous_light:         #Check for new light command
        if current_light == "No Light":         #all off
            GPIO.output(16, True)
            GPIO.output(20, True)
            GPIO.output(21, True)
        elif current_light == "Blue":           #blue on
            GPIO.output(16, False)
        elif current_light == "Yellow":         #yellow on
            GPIO.output(20, False)
        elif current_light == "Red":            #red on
            GPIO.output(21, False)
	
	#Activate Aural Alert
    if current_aural != previous_aural:          #Check for new aural command
        if current_aural == "No Alert":
            #do nothing
            track = 0
        elif current_aural == "Lightning1":
            Aural=subprocess.Popen(['omxplayer','./001lightning.mp3'], \
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True)
        elif current_aural == "Lightning2":
            Aural=subprocess.Popen(['omxplayer','./002lightning_passed.mp3'], \
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True)
        elif current_aural == "Lightning3": #nothing happens yet
            #do nothing
            track = 0
        elif current_aural == "Wind1":
            Aural=subprocess.Popen(['omxplayer','./003high_winds_approaching.mp3'], \
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True)
        elif current_aural == "Wind2":
            Aural=subprocess.Popen(['omxplayer','./004high_winds.mp3'],  \
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True)
        elif current_aural == "Wind3":
            Aural=subprocess.Popen(['omxplayer','./005high_winds_passed.mp3'], \
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True)

    #Update Current Signals		
    previous_light = current_light
    previous_aural = current_aural
    

#Gather Weather Data From WunderGround
#def gather_weather():
    #global f
    #f = urllib2.urlopen('http://api.wunderground.com/api/4bb2e676301d811b/conditions/q/WA/EVERETT.json')
    
#Return wind speed    
def gather_wind():
	#global f
	f = urllib2.urlopen('http://api.wunderground.com/api/4bb2e676301d811b/conditions/q/WA/EVERETT.json')
	json_string = f.read()
	parsed_json = json.loads(json_string)
	wind_speed = parsed_json['current_observation']['wind_mph']
	return float(wind_speed)
	
#Return Temp in F
def gather_temp():
	#global f
	f = urllib2.urlopen('http://api.wunderground.com/api/4bb2e676301d811b/conditions/q/WA/EVERETT.json')
	json_string = f.read()
	parsed_json = json.loads(json_string)
	temp_f = parsed_json['current_observation']['temp_f']
	return str(temp_f)

#Return wind direction
def gather_direction():
	#global f
	f = urllib2.urlopen('http://api.wunderground.com/api/4bb2e676301d811b/conditions/q/WA/EVERETT.json')
	json_string = f.read()
	parsed_json = json.loads(json_string)
	direction = parsed_json['current_observation']['wind_dir']
	return str(direction)


#GUI window formatting
class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        
        self.initUI() 
    
    #initialize GUI
    def initUI(self):
		#Send Alert Button
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        self.activate_button = QtGui.QPushButton('Send Alert', self)
        self.activate_button.setToolTip('This activates the selected alerts')
        self.activate_button.resize(self.activate_button.sizeHint())
        self.activate_button.move(125, 225)
        self.activate_button.clicked.connect(self.clicked_button)   #When clicked, call clicked_button
        
        #Visual Dropdown Menu
        self.lbl = QtGui.QLabel("Visual Alerts", self)
        self.visual = QtGui.QComboBox(self)
        self.visual.setToolTip('Select the visual alert you want to activate')
        
        #Add visual dropdown options
        self.visual.addItem("No Light")
        self.visual.addItem("Red")
        self.visual.addItem("Yellow")
        self.visual.addItem("Blue")
        
        self.visual.move(50, 75)
        self.lbl.move(52, 55)
        
        #When dropdown option selected, call visualchanged
        self.visual.activated[str].connect(self.visualchanged)
        
        #Aural Dropdown Menu
        self.lbl = QtGui.QLabel("Aural Alerts", self)
        self.aural = QtGui.QComboBox(self)
        self.aural.setToolTip('Select the aural alert you want to activate')
        
        #Add aural dropdown options
        self.aural.addItem("No Alert")
        self.aural.addItem("Lightning1")
        self.aural.addItem("Lightning2")  
        self.aural.addItem("Lightning3")  
        self.aural.addItem("Wind1")  
        self.aural.addItem("Wind2")  
        self.aural.addItem("Wind3")
        
        self.aural.move(200, 75)
        self.lbl.move(202, 55)
        
        #When dropdown option selected, call auralchanged
        self.aural.activated[str].connect(self.auralchanged)
        
        #Set Duration
        #Hour Dropdown Menu
        self.lbl = QtGui.QLabel("Hours", self)
        self.hour = QtGui.QComboBox(self)
        self.hour.setToolTip('Select the number of hours for the alert')
        self.hour.addItem("Select")
        
        #add hour dropdown options
        for i in xrange(24):
         self.hour.addItem(str(i))
        
        self.hour.move(50, 175)
        self.lbl.move(52, 155)
        
        #When dropdown option selected, call hourchanged
        self.hour.activated[str].connect(self.hourchanged)
        
        #Aural Dropdown Menu
        self.lbl = QtGui.QLabel("Minutes", self)
        self.minute = QtGui.QComboBox(self)
        self.minute.setToolTip('Select the number of minutes for the alert')
        self.minute.addItem("Select")
        
        #add minute dropdown options
        for i in xrange(60):
         self.minute.addItem(str(i))

        self.minute.move(200, 175)
        self.lbl.move(202, 155) 
        
        #when dropdown option selected, call minutechanged
        self.minute.activated[str].connect(self.minutechanged) 
        
        #Set up temperature display and set initial temperature
        #gather_weather()
        temp = gather_temp()
        self.temp_lbl = QtGui.QLabel("Current Temperature:", self)
        self.temp_lbl.move(0, 400)
        
        self.temperature = QtGui.QLabel("%s\xb0F" %temp, self)
        newfont = QtGui.QFont("Times", 14, QtGui.QFont.Bold)
        self.temperature.setFont(newfont)
        self.temperature.move(147, 398)
        
        #Set up Aural Display and display initial aural
        self.aural_lbl = QtGui.QLabel("Aural:", self)
        self.aural_lbl.move(0, 375)
        
        self.aural_alert = QtGui.QLabel("No Alert", self)
        newfont = QtGui.QFont("Times", 14, QtGui.QFont.Bold)
        self.aural_alert.setFont(newfont)
        self.aural_alert.move(45, 372)
        self.aural_alert.resize(100, 20)
        
        
        #Set up Wind Speed Display and display initial wind speed
        wind = gather_wind()
        direction = gather_direction()
        self.wind_lbl = QtGui.QLabel("Current Wind Speed:", self)
        self.wind_lbl.move(0, 430)
        
        self.wind_speed = QtGui.QLabel("%s mph %s" %(wind, direction), self)
        newfont = QtGui.QFont("Times", 14, QtGui.QFont.Bold)
        self.wind_speed.setFont(newfont)
        self.wind_speed.move(140, 426)
        self.wind_speed.resize(150, 20)
        
        #Setup Snowfall Height Display
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
        #Start timer to update GUI
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_gui)
        self.update_timer.start(1000) #1 sec interval
        
        #Start timer to update weather
        self.weather_timer = QtCore.QTimer()
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start(600000) #10 minute timer
                
    	#Activate Window
        self.setGeometry(150, 290, 400, 600)
        self.setWindowTitle('Severe Weather Warning System User Interface')
        self.show()
    
    #Update the wind speed, wind direction and temperature
    def update_weather(self):
    	global wind
    	global current_snow
    	#gather_weather()
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
    
    #Determine if wind speed should trigger an alert    
    def check_wind(self):
    	global current_light
    	global current_aural
    	global wind
    	if (wind) > 25 and (wind) <= 35:
    		current_light = "Blue"
    		current_aural = "Wind1"
    	elif (wind) > 35 and (wind) <= 50:
    		current_light = "Yellow"
    		current_aural = "Wind2"
    	elif (wind) > 50:
    		current_light = "Red"
    		current_aural = "Wind3"
    
    #Update the text in the GUI for communication and current alerts    
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
    
    #Set alert button actions	
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
