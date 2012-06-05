import pyglet
from pyglet.window import key
from pyglet.gl import *
import math

class App(object):
    def __init__(self,refresh=60):
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screens = display.get_screens()
        self.window = pyglet.window.Window(fullscreen=False,screen=screens[1])
        pyglet.clock.schedule_interval(self.update, 1.0/refresh)
        self.keyboard = key.KeyStateHandler()
        self.window.push_handlers(self.keyboard)
        self.window.set_handler("on_draw",self.on_draw)
    
    def update(self,dt):
        pass
        
    def on_draw(self):
        pass
        
    def run(self):
        pyglet.app.run()

class Camera(object):
    def __init__(self,position,scale=1,angle=0):
        self.x,self.y = position
        self.angle=angle
        self.scale=scale

    def focus(self, win_width, win_height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = win_width / win_height
        gluOrtho2D(-self.scale * aspect, # left
                   +self.scale * aspect, # right
                   -self.scale,          # bottom
                   +self.scale)          # top
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.x, self.y, +1.0, # camera  x,y,z
            self.x, self.y, -1.0, # look at x,y,z
            math.sin(self.angle), math.cos(self.angle), 0.0)

def draw_line(x1,y1,x2,y2,width=1,r=1,g=1,b=1):
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor3f(r,g,b)
    
    glLineWidth(width)
    glBegin(GL_LINES)
    glVertex2i( x1, y1)
    glVertex2i( x2, y2)
    glEnd()

    glDisable(GL_BLEND)
    glEnable(GL_TEXTURE_2D)