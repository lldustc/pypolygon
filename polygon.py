import math

class Vector:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __add__(self,v):
        return Vector(self.x+v.x,self.y+v.y)

    def __sub__(self,v):
        return Vector(self.x-v.x,self.y-v.y)

    def __mul__(self,s):
        return Vector(self.x*s,self.y*s)

    def __rmul__(self,s):
        return Vector(self.x*s,self.y*s)


    def dot(self,v):
        return self.x*v.x+self.y+v.y

    def length(self):
        return math.sqrt(self.dot(self))

    def cross_product(self,v):
        return self.x*v.y-self.y*v.x

    def norm(self):
        vec_len=self.length()
        if vec_len>0:
            return Vector(self.x/vec_len,self.y/vec_len)
        return Vector(0,0)

   
    def anticlockwise(self,v):
        '''
        if anticlockwise angle from self to v is positive
        
        '''
        return self.cross_product(v)>0
    
    def angle(self,v):
        ne1,ne2=self.norm(),v.norm()
        if ne1.length()>0 and ne2.length()>0:
            if ne1.anticlockwise(ne2):
                return math.acos(ne1.dot(ne2))
            else:
                return -math.acos(ne1.dot(ne2))
        return 0

    def rotate(self,a):
        '''
        rotate matrix M is [[cosa,-sina],[sina,cosa]],rotated vector is Mx
        '''
       return Vector(math.cos(a)*self.x-math.sin(a)*self.y,math.sin(a)*self.x+math.cos(a)*self.y)
        
    def in_line(self,v,eps):
        return self.length()<eps or v.length()<eps or abs(abs(self.norm().dot(v.norm()))-1)<eps

class Polygon:

    def __init__(self,vertexes,clockwise=True,eps=0.000001):
        '''
        change anticlockwise to clockwise
        '''
        self.vertexes=self.prepare(vertexes,clockwise)
        self.eps=eps

    def prepare(self,vertexes,clockwise):
        vs=vertexes[:]
        if vs[0]==vs[-1]:
            del vs[-1]
        if not clockwise:
            vs=list(reversed(vs))
        return [Vector(v[0],v[1]) for v in vs]

    def is_valid(self):
        for v1,v2 in self.neighbor_vertex_pairs():
            if (v1-v2).length()<self.eps:
                return False
        for v1,v2,v3 in self.neightbor_vertex_triples():
            if (v1-v2).dot(v3-v2)>self.eps and (v1-v2).in_line(v3-v2,self.eps):
                return False
        return True

    def neighbor_vertex_pairs(self):
        return zip(self.vertexes,self.vertexes[1:]+[self.vertexes[0]])

    def neightbor_vertex_triples(self):
        return zip(self.vertexes,self.vertexes[1:]+[self.vertexes[0]],self.vertexes[2:]+self.vertexes[0:2])

    def neighbor_edge_pairs(self):
        edges=[v2-v1 for v1,v2 in self.neighbor_edge_pairs()]
        return zip(edges,edges[1:]+[edges[0]])

    def hollow_vertexes(self):
        ss=[e1.anticlockwise(e2) for e1,e2 in self.neighbor_edge_pairs]
        hvs=[]
        for i,s in enumerate(ss):
            if s:hvs.append(i+1)
        return hvs

    def in_polygon(self,p):
        '''
        p in Polygon:the sum of angles which p to all vertexes is 2*pi
        p not in Polygon:0
        '''
        angles=[(v1-p).angle(v2-p) for v1,v2 in self.neighbor_vertex_pairs()]
        return abs(abs(sum(angles))-2*math.pi)<self.eps


