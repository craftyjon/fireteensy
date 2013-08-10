import coordinates

strand_str = """{
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


class fixturator:
    def __init__(self):
        self.address = 0
        self.strip = 0
        self.fixtures = """  "fixtures": [
    """
        


    def updateaddress(self):
        self.address += 1
        self.address = self.address % 4
        if self.address == 0:
            self.strip +=1
    
    def addStrip(self, pos1, pos2):
        self. fixtures += strand_str % (self.address, 60, pos1[0], pos1[1], pos2[0], pos2[1], self.strip) + ","
        self.updateaddress()

    def addStrips(self, base, *connected):
        for node in connected:
            self.addStrip(base, node)
        
    def generate(self):
        for i in range(5): #center
            pos1 = toFireMixCoords(idx0[0])
            pos2 = toFireMixCoords(idx1[i])
            pos3 = toFireMixCoords(idx1[(i+1)%5])
            self.addStrip(pos1, pos2)
 #           self.addStrip(pos2, pos3)    
        for i in range(5): #first layer
            base = toFireMixCoords(idx1[i])
            next_pos = toFireMixCoords(idx1[(i+1)%5])
            upleft = toFireMixCoords(idx2[((2*i) - 1) % 10])
            up = toFireMixCoords(idx2[(2*i)])
            upright = toFireMixCoords(idx2[((2*i) + 1) % 10])
            self.addStrips(base, next_pos, upleft, up, upright)
        for i in range(10): 
            base = toFireMixCoords(idx2[i])
            nodes = []
            nodes += [toFireMixCoords(idx2[((i+1) % 10)])] #next node
            if(i % 2 == 0): #corner node
                nodes += [toFireMixCoords(idx3[((i*3/2)-1) % 15])] #up and back
            if(i!=0):
                nodes += [toFireMixCoords(idx3[(((i-(i%2))*3/2)+(i%2)) % 15])] # up
            nodes += [toFireMixCoords(idx3[(((i-(i%2))*3/2)+(i%2) + 1) % 15])] # up and forward
            self.addStrips(base, *nodes)
        for i in range(13):
            self.addStrips(toFireMixCoords(idx3[(i+1)%15]), toFireMixCoords(idx3[(i+2)%15]))

    def generate(self, strand_dict):
        for strand in strand_dict.keys():
            struts = strand_dict[strand]
            strut_num = 0
            for strut in struts:
                self.add_strut(strut, strut_num, strand)
                strut_num = strut_num + 1
                

    def add_strut(self, strut_coords, strut_num, strand_num):
        start = toFireMixCoords(idxs[strut_coords[0][0]][strut_coords[0][1]])
        start[0] = 1000 - start[0]
        end = toFireMixCoords(idxs[strut_coords[1][0]][strut_coords[1][1]])
        end[0] = 1000 - end[0]
        self.addStrip(start, end, strut_num, strand_num)

    def addStrip(self, start, end, strut_num, strand_num):
        self. fixtures += strand_str % (strut_num, 60, start[0], start[1], \
                                            end[0], end[1], strand_num) + ","

        

def main():
    foo = fixturator() ; foo.generate(strands.strands); print foo.fixtures
    
# import coordinates; foo = coordinates.fixturator() ; foo.generate()
if __name__ == "__main__":
    main()



json = """{
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
  %s
    
  "labels_enable": false, 
  "locked": true, 
  "name": "Demo",
  "strand-settings": [
    {
        "color-mode": "BGR8",
        "enabled": true,
        "id": 0
    },
    {
        "color-mode": "BGR8",
        "enabled": true,
        "id": 1
    },
    {
        "color-mode": "BGR8",
        "enabled": true,
        "id": 2
    },
    {
        "color-mode": "BGR8",
        "enabled": true,
        "id": 3
    },
    {
        "color-mode": "BGR8",
        "enabled": true,
        "id": 4
    },
    {
        "color-mode": "BGR8",
        "enabled": true,
        "id": 5
    },
    {
        "color-mode": "BGR8",
        "enabled": true,
        "id": 6
    }
  ]
}
"""
