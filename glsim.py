#!/usr/local/bin/python
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT.freeglut import *
from OpenGL.GLUT import *
from numpy import array, interp, zeros
import numpy as np
from util.scene import Scene
import socket
import sys, time, os, Image, struct, time





# PyOpenGL 3.0.1 introduces this convenience module...
from OpenGL.GL.shaders import *

import time, sys
program = None
tex_name = None

scene = None

#for each strand, contains a list of the vertex of each pixel
strand_vertices = {} 


def getHeaders(data):
    strand = int(data[0])
    cmd = int(data[1])
    length = (int(data[3]) << 8) + int(data[2])
    return (strand, length, cmd)


# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL():                # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
    glDisable(GL_DEPTH_TEST)                # We'll just be doing a bunch of splatting
    glDisable(GL_ALPHA_TEST)                # We'll just be doing a bunch of splatting
    glEnable(GL_TEXTURE_2D)				# Enables texture mapping
    glEnable(GL_BLEND)
    glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading
    glPointSize(2)

    if not glUseProgram:
        print( 'Missing Shader Objects!' )
        sys.exit(1)
    global program
    global tex_name
    program = compileProgram(
        compileShader('''
            varying vec4 Color;
            varying vec2 vTexCoords;
            void main() {
                vTexCoords = gl_MultiTexCoord0.st;
                Color = gl_Color;
                gl_Position = gl_Vertex;
            }
        ''',GL_VERTEX_SHADER),
        compileShader('''
            uniform sampler2D myTex;
            
            varying vec4 Color;
            varying vec2 vTexCoords;
            void main() {
                gl_FragColor = Color + texture2D(myTex, vTexCoords).r;
            }
    ''',GL_FRAGMENT_SHADER),)

    success, tex_name = LoadRGBATexture ('/Users/jslocum/Pictures/NASA/102NIKON/DSCN4259.JPG')
    glBlendFuncSeparate(GL_ONE, GL_ONE, GL_ONE, GL_ZERO)


    
def LoadRGBATexture (path):
	""" // Load Image And Convert To A Texture
	path can be a relative path, or a fully qualified path.
	returns tuple of status and ID:
	returns False if the requested image couldn't loaded as a texture
	returns True and the texture ID if image was loaded
	"""
	# Catch exception here if image file couldn't be loaded
	try:
		# Note, NYI, path specified as URL's could be access using python url lib
		# OleLoadPicturePath () supports url paths, but that capability isn't critcial to this tutorial.
		Picture = Image.open (path)
	except:
		return False, 0

	glMaxTexDim = glGetIntegerv (GL_MAX_TEXTURE_SIZE)

	WidthPixels = Picture.size [0]
	HeightPixels = Picture.size [1]

	if ((WidthPixels > glMaxTexDim) or (HeightPixels > glMaxTexDim)):
		# The image file is too large. Shrink it to fit within the texture dimensions
		# support by our rendering context for a GL texture.
		# Note, Feel free to experiemnt and force a resize by placing a small val into
		# glMaxTexDim (e.g. 32,64,128).
		raise RuntimeError, "Texture image (%d by %d) is larger than supported by GL %d." % (WidthPixels, HeightPixels, glMaxTexDim)

	# Create a raw string from the image data - data will be unsigned bytes
	# RGBpad, no stride (0), and first line is top of image (-1)
	pBits = Picture.tostring("raw", "RGBX", 0, -1)
        
	texid = glGenTextures(1);
	glBindTexture(GL_TEXTURE_2D, texid);
	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)


        # // (Modify This If You Want Mipmaps)
	glTexImage2D(GL_TEXTURE_2D, 0, 3, WidthPixels, HeightPixels, 0, GL_RGBA, GL_UNSIGNED_BYTE, pBits);

	# Cleanup (this would all happen automatically upon return... just spelling it out)
	# // Decrements IPicture Reference Count
	Picture = None
	return True, texid					# // Return True (All Good)

timings = []
fps_timer = 0.0
def DrawGLScene():
    global sock, timings, fps_timer
    if program:
        glUseProgram(program)

    timings += [time.time()]
    if len(timings) > 60:
        timings = timings[1:]
    if timings[-1] - fps_timer > 0.1:
        fps = len(timings) / (timings[-1] - timings[0])
        glutSetWindowTitle("%f FPS" % fps)
        
        
    glBlendFuncSeparate(GL_ONE, GL_ONE, GL_ONE, GL_ZERO)
    glClear(GL_COLOR_BUFFER_BIT)

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, tex_name);


    for i in range(18):
        data, addr = sock.recvfrom(1024)
        data = struct.unpack('B'*len(data), data)
        strand, length, cmd = getHeaders(data)
        DrawLED_Strand(strand, data[4:724])

    
    # glBegin(GL_TRIANGLES)
    # glVertex4f(0.0, 0.0, 0.0, 1.0)
    # glMultiTexCoord2f(GL_TEXTURE0, 0.0, 0.0)
    # glColor4f(0.3,0.0,0.0, 1.0)
    # glVertex4f(1.0, 0.0, 0.0, 1.0)
    # glMultiTexCoord2f(GL_TEXTURE0, 1.0, 0.0)
    # glColor4f(0.0,0.1,0.0, 1.0)
    # glVertex4f(1.0, 1.0, 0.0, 1.0)
    # glMultiTexCoord2f(GL_TEXTURE0, 1.0, 1.0)
    # glColor4f(0.3,0.3,0.0, 1.0)
    
    # glEnd()

    
    glutSwapBuffers()

    
def ReSizeGLScene(Width, Height):
    pass
    

def getFixtureVertices(fixture):
    begin = (array(fixture.pos1()) - 500.0) / 500
    end = (array(fixture.pos2()) - 500.0) / 500
    pp = [0.0, 59.0]
    xp = [begin[0], end[0]]
    yp = [begin[1], end[1]]    
    return zip(interp(range(fixture.pixels()), pp, xp),
               interp(range(fixture.pixels()), pp, yp),
               zeros(fixture.pixels()),
               zeros(fixture.pixels())+1.0)

def InitStrandVertices():
    global scene
    global strand_vertices
    strands = scene.fixture_hierarchy()
    for strand in strands.keys():
        strand_vertices[strand] = []
        fixtures = strands[strand]
        for fixture in sorted(fixtures.keys()): #important to go from 0 to last
            strand_vertices[strand] += getFixtureVertices(fixtures[fixture])

    
def InitScene():
    global scene
    scene = Scene('./scenes/echodome.json')
    InitStrandVertices()

    
def DrawLED_Strand(strand, color_buffer):
    global strand_vertices
    color_buffer = array(color_buffer) / 255.0
    glBegin(GL_POINTS)
    pixel_vertices = strand_vertices[strand]
    for vertex, index in zip(pixel_vertices, range(len(pixel_vertices))):
        apply(glVertex4f, vertex)
        color = color_buffer[index*3:(index+1)*3]
        glColor4f(color[0], color[1], color[2], 1.0)
    glEnd()

sock=None
    
if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 3021))
    
    glutInit(sys.argv)
    #glutInitContextVersion(3, 2)
    glutInitWindowSize(1280, 1024)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_ALPHA | GLUT_DEPTH)
    glutCreateWindow("test")
    glutShowWindow( )
    glutDisplayFunc(DrawGLScene)
    # When we are doing nothing, redraw the scene.
    glutIdleFunc(DrawGLScene)
    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)
    
    # WTF opengl - this shit should work out of the box
    # major_version = glGetIntegerv(GL_MAJOR_VERSION)
    # minor_version = glGetIntegerv(GL_MINOR_VERSION)
    # print "Using OpenGL version %i, %i" % ( major_verison, minor_version )

    InitGL()
    InitScene()
    glutMainLoop( )

