import pyglet
from pyglet.gl import *

class Primitive(object):
    """
    A primitive object described by a list of vertices. Primitive vertices should be thought of as offsets
    from the origin of the Shape that they belong to. They are relative rather than absolute.
    """
    def __init__(self,verts,primtype,rotation=(0,0,0)):
        self.verts = [item for sublist in verts for item in sublist]
        self.primitive = primtype # eg. GL_TRIANGLES
        self.rot = rotation
                
    def _get_verts(self):
        """
        Join all of the points into a single list.
        """
        return self.verts
        
class Shape(object):
    """
    A shape made up of any number of Primitives and sub-shapes.
    """
    def __init__(self,primitives=[],position=(0,0,0),color=(1,1,1),rotation=(0,0,0),wireframe=False):
        """
        Arguments
            primitives: A list of Primitives that make up the Shape.
            position: A tuple. The 3 dimensional coordinate of the Shape in the format (x,y,z).
            color: A tuple. The 3-component RGB color of the shape. Colors are measured from 0-1.
            rotation: A tuple. The 3-dimensional rotation of the Shape in the format (x,y,z).
            wireframe: A bool. True to draw the shape using GL_LINE.
        """
            
        self.x,self.y,self.z = position
        self.colors = color
        self.primitives = primitives
        self.rot = rotation
        self.wireframe = wireframe
        self.sub_shapes = []
    
    def rotate(self,x,y,z):
        rx,ry,rz = self.rot
        rx += x
        ry += y
        rz += z
        self.rot=(rx,ry,rz)
        
    def translate(self,dx,dy,dz):
        self.x += dx
        self.y += dy
        self.z += dz
    
    def render(self):
        """
        Render the primitives of the shape.
        """
        glPushMatrix()
        glTranslatef(self.x,self.y,self.z)
        glRotatef(self.rot[0],1,0,0)
        glRotatef(self.rot[1],0,1,0)
        glRotatef(self.rot[2],0,0,1)
        #glTranslatef(-self.x,-self.y,-self.z)
        glColor3f(self.colors[0],self.colors[1],self.colors[2])
        if self.wireframe:
            glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );
            
        for prim in self.primitives:
            glPushMatrix()
            glRotatef(prim.rot[0],1,0,0)
            glRotatef(prim.rot[1],0,1,0)
            glRotatef(prim.rot[2],0,0,1)
            pyglet.graphics.draw(len(prim.verts),prim.primitive,('v3f',prim._get_verts()))
            glPopMatrix()
        for sub in self.sub_shapes:
            sub.render()
        
        if self.wireframe:
            glPolygonMode( GL_FRONT_AND_BACK, GL_FILL );
        glPopMatrix()


class RectangularPrism(Shape):
    def __init__(self,width=1,height=1,length=1,**kwargs):
        x,y,z = 0,0,0
        r = (x,y,z),(x+width,y,z),(x+width,y+height,z),(x,y+height,z),\
            (x,y,z+length),(x+width,y,z+length),(x+width,y+height,z+length),(x,y+height,z+length)
        self.width=width
        self.height=height
        faces = Primitive(r ,GL_QUADS)
        r = r[0],r[4], r[1],r[5], r[2],r[6], r[3],r[7]
        c = Primitive(r,GL_LINES)
        super(RectangularPrism,self).__init__([faces,c],**kwargs)