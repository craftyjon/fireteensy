#!/usr/local/bin/python

#For generating a Firemix configuration file to drive a geodesic dome with Teensys running octows2811 

import os
from packing import packer
from serial import Serial as OpenSerialPort
import pickle
import coordinates

num_strands = 16
struts_per_strand = 4
leds_per_strut = 60


def parse_dome_coords(string):
    coords = string.split(',')
    return [int(coords[0]), int(coords[1])]


class strand:
    def __init__(self):
        self.dome_coords = (0, 0)
        self.colors = 'RGBA'


#the end of the strut is address 0; the beggining is struts_per_strand-1
def getFrameIndex(strand, strut):
    return strand*struts_per_strand*leds_per_strut + strut*leds_per_strut


class teensyFrame:
    def __init__(self, struts_per_strand, leds_per_strut):
        self.frame = bytearray((leds_per_strut*struts_per_strand*8*3))
        self.header = bytearray(3)
        self.header[0] = '*'
        self.header[1] = 0x00
        self.header[2] = 0x00
        self.leds_per_strut = leds_per_strut
        self.struts_per_strand = struts_per_strand

    def clear(self):
        self.setAll([0,0,0])

    def setAll(self, color):
        for strand in range(8):
            for strut in range(4):
                self.setStrutColor(color, strand, strut)                
        
    def setStrutColor(self, color, strand, strut):
        offset = getFrameIndex(strand, strut)
        for i in range(self.leds_per_strut):
            self.frame[(offset + i)*3:(offset + i + 1)*3] = color[0:3]


    def setStrandColor(self, color, strand):
        for strut in range(self.struts_per_strand):
            self.setStrutColor(color, strand, strut)
            
    def setStrutGradient(self, color1, color2, strand, strut):
        print strut
        offset = getFrameIndex(strand, strut)
        print offset
        for i in range(60):
            color = [0,0,0]
            for j in range(3):
                color[j] = int(color2[j]*(i/59.0)) + int(color1[j]*((59-i)/59.0)) % 255
            self.frame[(offset + i)*3:(offset + i)*3 + 3] = color[0:3]



class teensyUtil:
    def __init__(self):
        self.strands = {} #dict from teensy numbers to active octo-strands
        self.teensyFiles = [] #list of files in /dev
        self.teensy_nums = []
        self.serials = {} #map from teensys numbers to serial connections
        self.serial_map = {} #map from serial connections to teensy numbers
        self.packer = packer(leds_per_strut*struts_per_strand)
        self.frame = teensyFrame(struts_per_strand, leds_per_strut)
        self.struts = {} #dict from (teensy number, strand, strut) to (front_coord, back_coord, color_format)
        self.strand_count = 0
        self.strand_map = {} #map from (teensy, octo-strand) to firemix strand


    def proceed(self):
        print "Proceded: y/n?"
        return self.queryYN()

    def queryYN(self):
        key = raw_input()
        while key not in "yn" or len(key) != 1:
            print "please answer y or n"
            key = raw_input()
        if key == 'y':
            return True
        else:
            return False

    
    def findTeensys(self):
        self.teensyFiles = ['/dev/' + x for x in os.listdir('/dev') if 'tty.usbmodem' in x]
        print "Found teensy list:"
        print self.teensyFiles
        return len(self.teensyFiles) == 3 and self.proceed()
        
    def connect(self):
        for f in self.teensyFiles:
            teensy_num = f[-5:]  #DIRTY HACK: Not safe, as teensy number might not be 5
            self.teensy_nums += [teensy_num]
            ser = OpenSerialPort(f, 256000)
            self.serials[teensy_num] = ser
            self.serial_map[ser] = teensy_num
        print "successfully connected to all teensys"

    def configure_strands(self):
        print "Please disconnect frame sync signals: hit return when ready"
        raw_input() #continues on enter
        self.mapStrandsToTeensys()
        self.clearAll()
        for teensy in self.teensy_nums:
            self.queryTeensyStrands(self.serials[teensy])

    def clearAll(self):
        for teensy in self.teensy_nums:
            serial = self.serials[teensy]
            self.frame.clear()
            self.sendFrame(serial)
            
    def sendFrame(self, serial):
        self.packer.packForOcto(self.frame.frame)
        serial.write(self.frame.header)
        serial.write(self.packer.cur_frame)
        
                

    def mapStrandsToTeensys(self):
        self.clearAll()
        for teensy in self.teensy_nums:
            serial = self.serials[teensy]
            print "Now testing teensy %s" % teensy
            self.strands[teensy] = []
            for strand in range(8):
                self.frame.clear()
                self.frame.setStrandColor([255,255,255], strand)
                self.sendFrame(serial)
                print "Is a strand now on? y/n"
                if self.queryYN():
                    self.strands[teensy] += [strand]
            self.clearAll()

    
        
    def queryTeensyStrands(self, serial):
        for strand in self.strands[self.serial_map[serial]]:
            for strut in range(struts_per_strand):
                self.queryStrut(serial, strand, strut)


    def queryStrut(self, serial, strand, strut):
        #(color format, dome_coordinates of close end, dome_coordinates of far end)
        teensy_num = self.serial_map[serial]
        color_format = self.getColorFormat(serial, strand, strut)
        front, back = self.getStrutCoordinates(serial, strand, strut)
        self.struts[(teensy_num, strand, strut)] = (front, back, color_format)


    def getColorFormat(self, serial, strand, strut):
        print "Color format not implemented: do this manually"
        return 'GRB'
        self.frame.clear()
        self.frame.setStrutColor([255, 0, 0], strand, strut)
        self.sendFrame(serial)
        print "Is the current strut red, green or blue?: r/g/b?"
        key = raw_input()
        while key not in "rgb" or len(key) != 1:
            print "please answer r or g"
            key = raw_input()
            if key == 'r':
                return 'rgb'
            else:
                return 'gbr'
            
    def getStrutCoordinates(self, serial, strand, strut):
        self.clearAll()
        self.frame.clear()
        self.frame.setStrutGradient([255, 255, 255], [0, 0, 255], strand, strut)
        self.sendFrame(serial)
        print "What are the dome coordinates of the white end of the strand?"
        print "Please use format (radius, circular position)."
        print "The top of the door is at (2, 0); the top of the pentagon to its left is (2,2) and its middle is (3, 3)"
        front_coords = parse_dome_coords(raw_input())
        while not front_coords:
            print "Please use format (radius, circular position)."
            front_coords = parse_dome_coords(raw_input())

        print "What are the dome coordinates of the colored end of the strand?"
        back_coords = parse_dome_coords(raw_input())
        while not back_coords:
            print "Please use format (radius, circular position)."
            back_coords = parse_dome_coords(raw_input())
        return front_coords, back_coords

    def exportFireTeensy(self):
        with open('./teensy-strands.pckl', 'w') as teensy_file:
            configuration = {}
            teensy_config = {}
            
            configuration['leds_per_strut'] = leds_per_strut
            configuration['struts_per_strand'] = struts_per_strand
            configuration['teensys'] = teensy_config
            for teensy in self.teensy_nums:
                teensy_config[teensy] = {}
                for strand in self.strands[teensy]:
                    teensy_config[teensy][self.strand_count] = strand
                    self.strand_map[(teensy, strand)] = self.strand_count
                    self.strand_count = self.strand_count + 1
            pickle.dump(configuration, teensy_file)
            return True

    def exportFireSim(self):
        with open('./echodome.firesim.json', 'w') as fs_file:
            fs_file.write((firesim_begin % self.generate_fixtures_json()) + (fire_end % self.generate_strands_json()))

    def exportFireMix(self):
        with open('./echodome.firemix.json', 'w') as fs_file:
            fs_file.write((firemix_begin % self.generate_fixtures_json()) + (fire_end % self.generate_strands_json()))

    def generate_fixtures_json(self):
        fixture_string = ""
        for teensy in self.teensy_nums:
            for strand in self.strands[teensy]: #get all octo-strands
                firemix_strand = self.strand_map[(teensy, strand)]
                for strut in range(struts_per_strand):
                    start, end, color_format = self.struts[(teensy, strand, strut)]
                    start = coordinates.domeToFiremixCoords(start)
                    end = coordinates.domeToFiremixCoords(end)                    
                    fixture_string += fire_fixtures % (strut, leds_per_strut, \
                                                           start[0], start[1], \
                                                           end[0], end[1], \
                                                           firemix_strand)
                    fixture_string +=','
        fixture_string = fixture_string[:-1]
        fixture_string += ']' # replace last comma with a close bracket
        return fixture_string
        
    def generate_strands_json(self):
        strand_string = ""
        for key in self.strand_map.keys():
            strand_string += fire_strands % ("RGB8", self.strand_map[key]) + ','
        strand_string = strand_string[:-1] #remove last comma
        return strand_string
    
    










firesim_begin = """{
  "backdrop_enable": false, 
  "backdrop_filename": "light_dome.png", 
  "bounding_box": [
    1000, 
    1000
  ], 
  "center": [
    500, 
    500
  ], 
  "extents": [
    1000, 
    1000
  ], 

  "fixtures": [
%s
    ],
"""

firemix_begin = """{
    "backdrop_enable": true, 
    "backdrop_filename": "light_dome.png", 
    "center": [
        500, 
        500
    ], 
    "extents": [
        1000, 
        1000
    ], 
    "file-type": "scene", 
   "fixtures": [
%s
    ],
"""

fire_fixtures = strand_str = """{
      "address": %i, 
      "pixels": %i, 
      "pos1": [
        %i, 
        %i
      ], 
      "pos2": [
        %i, 
        %i
      ], 
      "strand": %i, 
      "type": "linear"
    }"""

fire_strands = """        {
            "color-mode": "%s", 
            "enabled": true, 
            "id": %i
        }"""

fire_end = """    "labels_enable": true, 
    "locked": true, 
    "name": "Demo", 
    "strand-settings": [
%s
    ]
}
"""


if __name__=="__main__":
    tut = teensyUtil()
    while(not tut.findTeensys()):
        pass
    tut.connect()
    tut.configure_strands()
    tut.exportFireTeensy() #list of teensys and strand numbers 
    tut.exportFireSim()
    tut.exportFireMix()

