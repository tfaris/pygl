import glcommon
from pyglet.gl import *

class Light(object):
    def __init__(self,light_index=0,position=(0,0,0,1)):
        self.light_index = [GL_LIGHT0,GL_LIGHT1,GL_LIGHT2,GL_LIGHT3,GL_LIGHT4,GL_LIGHT5,GL_LIGHT6,GL_LIGHT7][light_index]
        self.position=position
        
    def toggle(self,on=True):
        if on:
            glEnable(GL_LIGHTING)
            glEnable(self.light_index)
        else:
            glDisable(self.light_index)
        self.render()
        
    def render(self):
        glLightfv(self.light_index,GL_POSITION,glcommon.iter_to_glfloats(self.position))

class AmbientLight(Light):
    def __init__(self,color=(0,0,0,1)):
        self.color = color
    def render(self):
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, glcommon.iter_to_glfloats(self.color))