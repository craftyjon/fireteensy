from numpy import array
from math import sin, cos, pi
import strands 

def torads(x):
    return x*pi/180

up = array([0, 1])
upleft = array([-cos(torads(18)), sin(torads(18))])
downleft = array([-sin(torads(36)), -cos(torads(36))])
upright = array([cos(torads(18)), sin(torads(18))])
downright = array([sin(torads(36)), -cos(torads(36))])
origin = array([0,0])

tlside = up - upleft
trside = upright - up
brside = downright - upright
bside = downleft - downright
blside = upleft - downleft

sides = [trside, brside, bside, blside, tlside]

idx0 = [origin]
idx1 = [up,upright,downright,downleft,upleft]



def getidx2(idx):
    if(idx % 2 == 0):
        return 2 * idx1[idx/2]
    else:
        return getidx2(idx-1) + sides[(idx-1)/2]


idx2 = [getidx2(i) for i in range(10)]


def getidx3(idx):
    if(idx % 3 == 0):
        return 3 * idx1[idx/3]
    else:
        offset = idx % 3;
        return getidx3(idx-offset) + offset*sides[(idx-offset)/3]



idx3 = [getidx3(i) for i in range(15)]
indexes = {0:idx0, 1:idx1, 2:idx2, 3:idx3}

idxs = [idx0, idx1, idx2, idx3]

address = 0
strip = 0



def rawToFireMixCoords(idx):
    coords = ((idx * 150) + array([500,500]))
    return array([round(coords[0]), round(coords[1])])


def domeToFiremixCoords(dome_coords):
    print dome_coords
    idx = idxs[dome_coords[0]][dome_coords[1]]
    coords = ((idx * 150) + array([500,500]))
    return array([round(coords[0]), round(coords[1])])
