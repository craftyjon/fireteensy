#!/usr/local/bin/python
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT.freeglut import *
from OpenGL.GLUT import *
from numpy import array
import sys
glutInit(sys.argv)
#glutInitContextVersion(3, 2)
glutInitWindowSize(1280, 1024)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_ALPHA | GLUT_DEPTH)
glutCreateWindow("test")
#glutReshapeWindow(1280, 1024)
glutShowWindow( )


# PyOpenGL 3.0.1 introduces this convenience module...
from OpenGL.GL.shaders import *

import time, sys
program = None


# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL():                # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
    glDisable(GL_DEPTH_TEST)                # We'll just be doing a bunch of splatting
    glDisable(GL_ALPHA_TEST)                # We'll just be doing a bunch of splatting
    glEnable(GL_BLEND)
    glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading


    if not glUseProgram:
        print( 'Missing Shader Objects!' )
        sys.exit(1)
    global program
    program = compileProgram(
        compileShader('''
            varying vec4 Color;
            void main() {
                Color = gl_Color;
            }
        ''',GL_VERTEX_SHADER),
        compileShader('''
            varying vec4 Color;
            void main() {
                gl_FragColor = Color;
            }
    ''',GL_FRAGMENT_SHADER),)


    glBlendFuncSeparate(GL_ONE, GL_ONE, GL_ONE, GL_ZERO)
    
def DrawGLScene():
    glBlendFuncSeparate(GL_ONE, GL_ONE, GL_ONE, GL_ZERO)
    glClear(GL_COLOR_BUFFER_BIT)
    
    glBegin(GL_TRIANGLES)
    glVertex4f(0.0, 0.0, 0.0, 1.0)
    glMultiTexCoord2f(0.0, 0.0)
    glColor4f(0.3,0.0,0.0, 1.0)
    glVertex4f(1.0, 0.0, 0.0, 1.0)
    glMultiTexCoord2f(1.0, 0.0)
    glColor4f(0.0,0.1,0.0, 1.0)
    glVertex4f(1.0, 1.0, 0.0, 1.0)
    glMultiTexCoord2f(1.0, 1.0)
    glColor4f(0.3,0.3,0.0, 1.0)


    glVertex4f(0.0, 0.0, 0.0, 1.0)
    glColor4f(0.3,0.0,0.0, 1.0)
    glVertex4f(1.0, 0.0, 0.0, 1.0)
    glColor4f(0.0,0.1,0.0, 1.0)
    glVertex4f(1.0, 1.0, 0.0, 1.0)
    glColor4f(0.3,0.3,0.0, 1.0)


    glVertex4f(0.0, 0.0, 0.0, 1.0)
    glColor4f(0.3,0.0,0.0, 1.0)
    glVertex4f(1.0, 0.0, 0.0, 1.0)
    glColor4f(0.0,0.1,0.0, 1.0)
    glVertex4f(1.0, 1.0, 0.0, 1.0)
    glColor4f(0.3,0.3,0.0, 1.0)
    glEnd()

    
    glutSwapBuffers()

def ReSizeGLScene(Width, Height):
    pass
    

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
glutMainLoop( )


while True:
    pass
