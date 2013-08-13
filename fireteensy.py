#!/usr/local/bin/python
#read in configuration/callibration file



#check that all teensy's are available and can be communicated with

#start listening on network socket for firemix data

#loop forever: parse firemix data and send it to teensy's

#http://stackoverflow.com/questions/12254378/how-to-find-the-serial-port-number-on-mac-os-x
#http://stackoverflow.com/questions/16077912/python-serial-how-to-use-the-read-or-readline-function-to-read-more-than-1-char
#listen on port 3021 and report the received commands


def getHeaders(data):
    strand = int(data[0])
    cmd = int(data[1])
    length = (int(data[3]) << 8) + int(data[2])
    return (strand, length, cmd)

import struct
import socket
import serial
import pickle
import time
from profilehooks import profile
from packing import packer


class TeensyRouter:
    def __init__(self, config_path):
        self.config_path = config_path
        self.strands = {} #map from strand numbers to teensy, octo strand pairs
        self.port = 3021
        self.address = '127.0.0.1'
        self.frames = {}
        self.serials = {}
        self._net_connected = False
        
    def initialize(self):
        return self.readConfig() and self.connectTeensys() and self.initUDP()

    def readConfig(self):
        #read in the file
        print "reading configuration file from %s" % self.config_path
        with open(self.config_path, 'rb') as cfg:
            configuration = pickle.load(cfg)
            if 'teensys' not in configuration.keys():
                return False
            self.teensy_config = configuration['teensys']

        
        self.leds_per_strut = configuration['leds_per_strut']
        self.struts_per_strand = configuration['struts_per_strand']
        self.leds_per_strand = self.leds_per_strut * self.struts_per_strand
        self.packer = packer(self.leds_per_strut * self.struts_per_strand)

        #map firemix strands to teensy/octo strand pairs
        for teensy_num in self.teensy_config.keys(): 
            self.frames[teensy_num] = bytearray(8*3*self.leds_per_strand)
            strand_dict = self.teensy_config[teensy_num]
            for key in strand_dict.keys():
                strand = key
                octo_strand = strand_dict[key]
                self.strands[strand] = (teensy_num, octo_strand)
        return True
            
    def connectTeensys(self):
        if not len(self.teensy_config.keys()) == 3:
            return False
        self.serials = {}
        for teensy_num in self.teensy_config.keys():
            try:
                self.serials[teensy_num] = \
                    serial.Serial('/dev/tty.usbmodem'+teensy_num, 256000)
                print "connected to teensy %s" % teensy_num
            except:
                print "could not connect to all teensys: disconnecting any open connections"
                self.shutdown()
                return False
        print "successfully connected to teensys"
        return True

    def initUDP(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.address, self.port))
        print "successfully connected to UDP"
        self._net_connected = True
        return True

    def serve_forever(self):
        while True:
            for i in range(18):
                data, addr = self.socket.recvfrom(1024)
                data = struct.unpack('B'*len(data), data)
                strand, length, cmd = getHeaders(data)
                #print strand, length, cmd
                teensy, octo_strand = self.strands[strand]
                #print teensy, octo_strand
                bps = 3*self.leds_per_strand
                #octo-strands are 0-indexed
                self.frames[teensy][octo_strand*bps:(octo_strand+1)*bps] = data[4:bps+4]
                #print "setting frame data from byte %i to %i" % (octo_strand*bps, (octo_strand+1)*bps)
            header = bytearray(3)
            header[1] = 0x00
            header[2] = 0x00
            commands = ['*', '*', '*']
            for command, teensy in zip(commands, self.serials.keys()):
                header[0] = command
                self.sendFrame(header, teensy)


            
    def serve_once(self):
        for x in range(1):
            for i in range(18):
                data, addr = self.socket.recvfrom(1024)
                data = struct.unpack('B'*len(data), data)
                strand, length, cmd = getHeaders(data)
                #print strand, length, cmd
                teensy, octo_strand = self.strands[strand]
                #print teensy, octo_strand
                bps = 3*self.leds_per_strand
                #octo-strands are 0-indexed
                self.frames[teensy][octo_strand*bps:(octo_strand+1)*bps] = data[4:bps+4]
                #print "setting frame data from byte %i to %i" % (octo_strand*bps, (octo_strand+1)*bps)
            header = bytearray(3)
            header[1] = 0x00
            header[2] = 0x00
            commands = ['*', '*', '*']
            for command, teensy in zip(commands, self.serials.keys()):
                header[0] = command
                self.sendFrame(header, teensy)

                
    def sendFrame(self, header, teensy):
        self.packer.packForOcto(self.frames[teensy])
        self.serials[teensy].write(header)
        self.serials[teensy].write(self.packer.cur_frame)

    def shutdown(self):
        for k in self.serials.keys(): 
            serials[k].close() #make sure to release any currently used ports
        if self._net_connected:
            self.socket.close()    #close the socket




t = TeensyRouter('./teensy-strands.pckl')

def shutdown(arg1, arg2):
    t.shutdown()
    exit(0)

import signal
import sys
signal.signal(signal.SIGINT, shutdown)

    
if __name__ == "__main__":
    if not(t.initialize()):
        while 1:
            pass
        exit(-1)
    t.serve_forever()
    
    
