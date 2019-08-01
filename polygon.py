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

    def __init__(self,vertexes,eps=0.000001):
        '''
        change anticlockwise to clockwise
        '''
        self.eps=eps
        self.vertexes=self.prepare(vertexes)

    def prepare(self,vertexes):
        vs=vertexes[:]
        if vs[0]==vs[-1]:
            del vs[-1]
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

    def is_clockwise(self):
        def get_max_x_index():
            index,max_x=0,self.vertexes[0].x
            for i,v in enumerate(self.vertexes[1:]):
                if v.x>max_x:
                    index,max_x=i+1,v.x
            return index
        ind=get_max_x_index()
        if ind==0:
            v1,v2,v3=self.vertexes[-1],self.vertexes[0],self.vertexes[1]
        else:
            v1,v2,v3=self.vertexes[ind-1],self.vertexes[ind],self.vertexes[( ind+1 )%len(self.vertexes)]
        return not (v2-v1).anticlockwise(v3-v2)

    def hollow_vertexes(self):
        ss=[ ( e1.anticlockwise(e2),e1.in_line(e2.self.eps) ) for e1,e2 in self.neighbor_edge_pairs]
        hvs=[]
        clockwise=self.is_clockwise()
        for i,(s,is_line) in enumerate(ss):
            if (not is_line) and ((clockwise and s) or ((not clockwise) and (not s))):
                hvs.append(i+1)
        return hvs

    def in_polygon(self,p):
        '''
        p in Polygon:the sum of angles which p to all vertexes is 2*pi
        p not in Polygon:0
        '''
        angles=[(v1-p).angle(v2-p) for v1,v2 in self.neighbor_vertex_pairs()]
        return abs(abs(sum(angles))-2*math.pi)<self.eps

    def in_edge(self,p):
        in_range=lambda p1,p2:min(p1.x,p2.x)<=p.x<=max(p1.x,p2.x) and \
                min(p1.y,p2.y)<=p.y<=max(p1.y,p2.y)
        for p1,p2 in self.neighbor_vertex_pairs():
            if (p-p1).in_line(p-p2,self.eps) and in_range(p1,p2):
                return True
        return False

    def extend(self,s):
        def extend_one_vertex(v1,v2,v3):
            '''
            v1 prev v2,v2 prev v3
            '''
            ne1,ne2=(v1-v2).norm(),(v3-v2).norm()
            clockwise=self.is_clockwise()
            if ne1.in_line(ne2):
                rotate_angle=1/2*math.pi
                if not clockwise:rotate_angle=-rotate_angle
                return v2 + ( ne2.rotate(rotate_angle)*s )
            else:
                sl=s/math.sqrt(1-ne1.dot(ne2)**2)
                if (clockwise and ne1.anticlockwise(ne2)) or \
                    ((not clockwise) and (not ne1.anticlockwise(ne2))):
                    sl=-sl
                se1,se2=ne1*sl,ne2*sl
                return v2+(se1+se2)
        vs=[extend_one_vertex(v1,v2,v3) for v1,v2,v3 in self.neightbor_vertex_triples()]
        return Polygon([(v.x,v.y) for v in vs])

    def tolist(self):
        return [(v.x,v.y) for v in self.vertexes]
