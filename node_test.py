import time
import serial
import struct

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()

print 'Testing will now commence'

import struct

start=255
light=5
track=1
snow =3

values = (start, light, track, snow)

string = ''

for i in values:
    string += struct.pack('!B',i)

while 1 :
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        ser.write(string)
        print values
        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        #time.sleep(.5)
        #ser.flush() 
        out1 = ser.read(1) 
        out2 = ser.read(1) 
	print out1, ord(out2)
        time.sleep(.5)
