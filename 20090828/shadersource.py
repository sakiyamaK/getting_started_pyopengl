from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from OpenGL.GL.ARB.shader_objects import *
from OpenGL.GL.ARB.vertex_shader import *
from OpenGL.GL.ARB.fragment_shader import *


def read_shader_source(shader, file):
    print("glShaderSourceARB:", bool(glShaderSourceARB))
    source = '\n'.join(open(file, 'r').readlines())
    glShaderSourceARB( shader, source)
    glCompileShaderARB(shader)
    return shader

if __name__ == "__main__":
    print("test")