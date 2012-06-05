"""
A python implementation of the game Tetris in OpenGL, using pyglet.

[INCOMPLETE!]
"""

import os,sys
sys.path.append(os.path.abspath("."))
from pyglet.window import key
from tfgl.glapp import App,draw_line
from tfgl.shapes import *
import random,math

class Tetrinimo(Shape):
    """
    A Tetrinimo is a shape used in the game Tetris.
    """
    blocks = ()
    color=[1,0,1]
    def __init__(self,**kwargs):
        super(Tetrinimo,self).__init__(**kwargs)
        self.width = len(max(self.blocks,key=lambda x:len(x)))
        self.height = len(self.blocks)
        
        self.tetr_x=0
        self.tetr_y=0
        self.tetr_z=-2
        for block_pos in self.blocks:
            r_prism = RectangularPrism(position=(block_pos[0],block_pos[1]-1,0),wireframe=False,color=self.color)
            self.sub_shapes.append(r_prism)
        #center = RectangularPrism(position=(0,0,0))
        #self.sub_shapes.append(center)

    def rotate(self,clockwise=True):
        rx,ry,rz = self.rot        
        rz = rz+90 if clockwise else rz-90
        self.rot = (rx,ry,rz)
        
    def get_y(self):
        # self.y is centroid y
        c_y = min(self.sub_shapes,key=lambda sub_sh: sub_sh.y+sub_sh.height)
        return c_y.y+self.y-.5
        
        
    def set_x(self,val):
        self.tetr_x = val//1
    def get_x(self):
        return self.tetr_x
    def set_y(self,val):
        self.tetr_y = val//1
    def get_y(self):
        return self.tetr_y
    def set_z(self,val):
        self.tetr_z = val//1
    def get_z(self):
        return self.tetr_z
        
    x = property(get_x,lambda s,v: s.set_x(v))
    y = property(get_y,lambda s,v: s.set_y(v))
    z = property(get_z,lambda s,v: s.set_z(v))
    
class T_I(Tetrinimo):
    blocks=((-.5,2),(-.5,1),(-.5,0),(-.5,-1))
    color=(0,255.0/255,255.0/255)
class T_J(Tetrinimo):
    blocks=((-.5,1.5),(-.5,.5),(-.5,-.5),(-1.5,-.5))
    color=(0,0,255.0/255)
class T_L(Tetrinimo):
    blocks=((-.5,1.5),(-.5,.5),(-.5,-.5),(.5,-.5))
    color=(255.0/255,165.0/255,0)
class T_O(Tetrinimo):
    blocks=((-1,1),(0,1),(-1,0),(0,0))
    color=(255.0/255,255.0/255,0)
    
    def set_x(self,val):        
        self.tetr_x = val//1+.5
    
class T_S(Tetrinimo):
    blocks=((-.5,1),(.5,1),(-1.5,0),(-.5,0))
    color=(0,255.0/255,0)    
class T_T(Tetrinimo):
    blocks=((-.5,1.5),(-1.5,0.5),(-.5,0.5),(.5,0.5))
    color=(170.0/255,0,255.0/255)    
class T_Z(Tetrinimo):
    blocks=((-1.5,1),(-.5,1),(-.5,0),(.5,0))
    color=(255.0/255.0,0,0)

class TetrisApp(App):
    tetrinimos = ( T_O,T_J,T_L,T_I,T_S,T_Z,T_T )

    def __init__(self):
        super(TetrisApp,self).__init__()
        self.view_ortho = True
        pyglet.clock.schedule_interval(self.update_blocks, 1.0/1)
        self.window.set_handler("on_key_release",self.on_key_release)        
        
        self.live_blocks = []
        self.fell_blocks = []
        
        self.width = 25
        self.height = self.width * .75
        
    def generate_block(self):
        block = random.choice(self.tetrinimos)()
        block.y = 15
        block.x = self.width/2.0
        self.live_blocks.append(block)    
        
    def on_draw(self):
        glClearColor(1,1,1,1) 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
        glMatrixMode(GL_PROJECTION)    
        glLoadIdentity()   
                
        #gluPerspective(60.0, self.width/self.height, .01, 100.0)        
        #glOrtho(-12.5, 12.5, 0.1, 25, 1, 100)
        glOrtho(0,self.width,0,self.height,1,100)
            
        glTranslatef(0,0,-10)
        draw_line(0,2,self.width,2,width=2,r=0,g=0,b=0)
        glTranslatef(0,0,10)        
        if not self.view_ortho:
            glLoadIdentity()
            glFrustum(0,self.width,0,self.height,1,100)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()  
        # gluLookAt(0,0,0,
                  # 0,0,-2,
                  # 0,1,0)
                
        for block in self.fell_blocks:
            block.render()
        
        for block in self.live_blocks:
            block.render()
        
    
    def update_blocks(self,dt):
        for live_block in self.live_blocks:
            live_block.translate(0,-1,0)
            y = live_block.get_y()
            if y <= 2:
                self.live_blocks.remove(live_block)
                self.fell_blocks.append(live_block)
                self.generate_block()
        
    def on_key_release(self,symbol, modifiers):
        if symbol == key.UP:
            [b.rotate(False) for b in self.live_blocks]
        elif symbol == key.RIGHT:
            [b.translate(1,0,0) for b in self.live_blocks]
        elif symbol == key.LEFT:
            [b.translate(-1,0,0) for b in self.live_blocks]
        elif symbol == key.DOWN:
            [b.translate(0,-1,0) for b in self.live_blocks]
        elif symbol == key.Q:
            self.view_ortho = not self.view_ortho
        
    def run(self):
        self.generate_block()
        super(TetrisApp,self).run()

if __name__ == "__main__":        
    app = TetrisApp()
    app.run()








