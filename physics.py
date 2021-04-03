from EulerLib.geometry import Point, Vector

class Point3D(Point):
    def __init__(self,x:float,y:float,z:float):
        super().__init__(x,y)
        self.z = z

    def __add__(self,other):
        return Point3D(self.x+other.x,self.y+other.y,self.z+other.z)
        
    def __sub__(self,other):
        return Point3D(self.x-other.x,self.y-other.y,self.z-other.z)

class Vector3D(Vector):
    def __init__(self,x:float,y:float,z:float):
        super().__init__(x,y)
        self.z = z

class PhysicsObject:
    def __init__(self,position:Point=Point(0,0),velocity:Vector=Vector(0,0),acceleration:Vector=Vector(0,0),update_position_first=True):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self._update_position_first = update_position_first

    def step(self):
        if self._update_position_first:
            self.position += self.velocity
            self.velocity += self.acceleration
        else:
            self.velocity += self.acceleration
            self.position += self.velocity
