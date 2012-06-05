"""
Commonly used routines for python OpenGL.
"""

from pyglet.gl import GLfloat

def iter_to_glfloats(iterable):
    """
    Converts a python iterable into a c_float_Array.
    """
    return (GLfloat*len(iterable))(*iterable)
