###############################################################################
# Raspberry Pi Alert Handler
#
# Created By: Antonio Perez
#
# Date: 3/31/16
#
###############################################################################

#Import all libraries
import urllib2
import threading
import subprocess
import RPi.GPIO as GPIO

#Create Global Variables
global current_light
global current_aural
global previous_light
global previous_aural

current_light = 'Initial'
current_aural = 'Initial'
previous_light = 'Initial'
previous_aural = 'Initial'

#Setup GPIOS
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

GPIO.output(16, True)
GPIO.output(20, True)
GPIO.output(21, True)

def get_alerts():
    global current_light
    global current_aural
    current_light = urllib2.urlopen('http://web.engr.oregonstate.edu/~pereza/light.txt').read()
    current_aural = urllib2.urlopen('http://web.engr.oregonstate.edu/~pereza/siren.txt').read()
    #current_light = open('light.txt','r')
    #current_aural = open('siren.txt','r')
    
def set_alerts():
    global current_light
    global current_aural
    global previous_light
    global previous_aural
    
    if current_light != previous_light:
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
        print current_light
            
    if current_aural != previous_aural:
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
        print current_aural
        
    previous_light = current_light
    previous_aural = current_aural
    
    
def f():
        get_alerts()
        set_alerts()
        threading.Timer(2,f).start()
    
def main():
    f()
    
if __name__ == '__main__':
    main()