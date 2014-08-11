class packer:
    def __init__(self, strip_length, color_format = 'GRB'):
        self.cur_frame = bytearray(strip_length*8*3)
        self.color_format = color_format
        self.strip_length = strip_length
        self.swap = bytearray(8)
        
    def getFrameOctuplet(self, frame, index):
        lst = []
        for strand in range(8):
            lst += [frame[index + strand*240*3]]
        return lst
    
    #@profile
    def packForOcto(self, frame):
        for led_channel in range(self.strip_length*3): #for each color channel octuplet
            self.cur_frame[led_channel*8:(led_channel+1)*8] = \
                self.packOctoBits(self.getFrameOctuplet(frame, led_channel))
        if self.color_format == 'GRB':
            for color_index in range(self.strip_length):
                idx = color_index * 3
                self.swap_space = self.cur_frame[idx*8:(idx+1)*8] #grab red data
                self.cur_frame[idx*8:(idx+1)*8] = \
                    self.cur_frame[(idx+1)*8:(idx+2)*8] #write green into red's spot
                self.cur_frame[(idx+1)*8:(idx+2)*8] = self.swap_space #write red into green's spot

                
    #@profile
    def packOctoBits(self, byte_list):
        octo_bytes = bytearray(8)
        index = 0
        for m in range(8):
            mask = 1 << (7-m)
            byte = 0x00
            for i in range(8):
                if (mask & byte_list[i]):
                    byte |= (1 << i)
            octo_bytes[index] = byte
            index = index + 1
        return octo_bytes
