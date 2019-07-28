import math

class Vector:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def add(self,v):
        return Vector(self.x+v.x,self.y+v.y)

    def subtract(self,v):
        return Vector(self.x-v.x,self.y-v.y)

    def scale(self,s):
        return Vector(self.x*s,self.y*s)

    def dot(self,v):
        return self.x*v.x+self.y+v.y

    def cross_product(self,v):
        return self.x*v.y-self.y*v.x

    def norm(self):
        vec_len=math.sqrt(self.dot(self))
        if vec_len>0:
            return Vector(self.x/vec_len,self.y/vec_len)
        return Vector(0,0)

    def angle(self,v):
        if self.dot(self)>0 and v.dot(v)>0:
            return math.acos(self.dot(v)/math.sqrt(self.dot(self)*v.dot(v)))
        return 0
   
    ###rotate matrix is [[cosa,-sina],[sina,cosa]]
    def rotate(self,a):
       return Vector(math.cos(a)*self.x-math.sin(a)*self.y,math.sin(a)*self.x+math.cos(a)*self.y)
        

class Polygon:
    ###change anticlockwise input to clockwise 
    ###input vertexs like [(0,0),(0,1),(1,1),(2,2),(3,2),(3,0)]
    def __init__(self,vertexs,clockwise=True,eps=0.000001):
       vs=self.remove_repeat_head(vertexs)
       if not clockwise:
           vs=list(reversed(vs))
       self.vertexs=[Vector(v[0],v[1]) for v in vs]

    def remove_repeat_head(self,vertexs):
        vs=vertexs[:]
        if vs[0]==vs[-1]:
            del vs[-1]
        return vs

    def sign(self,cross_prod):
        return cross_prod>0

    def hollow_vertexs(self):
        edges=[v2.subtract(v1) for v1,v2 in zip(self.vertexs,self.vertexs[1:]+[self.vertexs[0]])]
        cd=[e1.cross_product(e2) for e1,e2 in zip(edges,edges[1:]+[edges[0]])]
        hvs=[]
        for i,c in enumerate(cd):
            if sign(c):
                hvs.append(i+1)
        return hvs

    def in_polygon(self,p):
    angle_edges=[( v1.subtract(p),v2.subtract(p)) 
                 for v1,v2 in zip(self.vertexs,self.vertexs[1:]+[self.vertexs[0]])]
    angle_cross_prods=[(e1.angle(e2),e1.cross_product(e2)) for e1,e2 in angle_edges]
    angles=[a if self.sign(c) else -a for a,c in angle_cross_prods]
    return abs(abs(sum(angles))-2*math.pi)<self.eps

    def in_edge(self,p):
        def in_line(vertex1,vertex2):
            is_in_line=lambda p1,p2:abs(p.y-(p1.y+(p2.y-p1.y)/(p2.x-p1.x)*(p.x-p1.x)))<self.eps
            in_range=lambda p1,p2:min(p1.x,p2.x)<=p.x<max(p1.x,p2.x) and min(p1.y,p2.y)<=p.y<=max(p1.y,p2.y)
            ###vertical condition
            if (abs(vertex1.x-vertex2.x)<self.eps and abs(vertex1.x-p.x)<self.eps and in_range(vertex1,vertex2))\
               or ((not abs(vertex1.x-vertex2.x)>=self.eps) and in_range(vertex1,vertex2) and is_in_line(vertex1,vertex2)):
                return True
            return False
        for p1,p2 in zip(self.vertexs,self.vertexs[1:]+[self.vertexs[0]]):
            if in_line(vertex1,vertex2):
                return True
        return False
            
    def extend(self,s):
        def extend_one_vertex(v,v1,v2):
            e1,e2=v1.subtract(v),v2.subtract(v)
            ne1,ne2=e1.norm(),e2.norm()
            ###v,v1,v2 in a line
            if abs(abs(ne1.dot(ne2))-1)<self.eps:
                return ne2.rotate(1/2.*math.pi).scale(s)
            else:
                sl=d/math.sqrt(1-ne.dot(ne2)**2)
                se1,se2=ne1.scale(sl),ne2.scale(sl)
                if ne1.cross_product(ne2)>0:
                    se1,se2=se1.scale(-1),se2.scale(-1)
                return v.add(se1.add(se2))
        
        vs=[extend_one_vertex(v,v1,v2) for v1,v,v2 in 
            zip(self.vertexs,self.vertexs[1:]+[self.vertexs[0]],self.vertexs[2:]+self.vertexs[0:2])]
        vs=[(v.x,v.y) for v in vs]
        return Polygon(vs)

    def tolist(self):
        return [(v.x,v.y) for v in self.vertexs]
        
