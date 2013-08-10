#!/usr/local/bin/python

import serial
import time
from profilehooks import profile
from packing import packer

ser1 = serial.Serial('/dev/tty.usbmodem14421', 256000)
ser2 = serial.Serial('/dev/tty.usbmodem12151', 256000)
ser3 = serial.Serial('/dev/tty.usbmodem12161', 256000)
frame = bytearray((240*8*3))
header = bytearray(3)
header[0] = '*'
header[1] = 0x00
header[2] = 0x00
#frame[0] is the beginning of the strand !?!?!?
#and frame[239*3] is the end....
for i in range(240*8): # should just be the first strut
    frame[(0+i)*3] = 0#(i) % 240 #ends should be red
    frame[(0+i)*3+1] = 0
    frame[(0+i)*3+2] = 255#(240-i) % 240 # beginnings should be blue


num_strand_bits = 240*8*3
    

def incFrame(frame):
    for i in range(240*8):
        frame[i*3] = (frame[i*3] + 1) % 256
        frame[i*3+1] = frame[i*3+1]
        frame[i*3+2] = (frame[i*3+2] - 1) % 256
        


@profile 
def sendFrame(frame):
    p.packForOcto(frame)
    ser1.write(header)
    ser1.write(p.cur_frame)
    ser2.write(header)
    ser2.write(p.cur_frame)
    ser3.write(header)
    ser3.write(p.cur_frame)


#ser.read(1)

p = packer(240)
print header
print p.cur_frame[0:100]
print len(p.cur_frame)

for i in range(5):
    sendFrame(frame)
    #incFrame(frame)

ser1.close()
ser2.close()
ser3.close()
    

