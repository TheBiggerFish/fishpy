from random import randint
from typing import Final, Optional, Tuple


class Point:
    def __init__(self,x:float,y:float):
        self.x = x
        self.y = y

    def __add__(self,other:'Point') -> 'Point':
        return Point(self.x+other.x,self.y+other.y)

    def __sub__(self,other:'Point') -> 'Point':
        return Point(self.x-other.x,self.y-other.y)

    def __neg__(self) -> 'Point':
        return Point(-self.x,-self.y)

    def __eq__(self,other:'Point') -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash(str(self.x * (10**10) + self.y))

    def __lt__(self,other:'Point') -> bool:
        return self.y < other.y and self.x < other.x

    def __gt__(self,other:'Point') -> bool:
        return not self < other and not self == other

    def __le__(self,other:'Point') -> bool:
        return self.y <= other.y and self.x <= other.x

    def __str__(self) -> str:
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __repr__(self) -> str:
        return f'Point{str(self)}'

    def __mul__(self,scalar:float) -> 'Point':
        return Point(self.x*scalar,self.y*scalar)

    def __truediv__(self,scalar:float) -> 'Point':
        return Point(self.x/scalar,self.y/scalar)

    def __floordiv__(self,scalar:float) -> 'Point':
        return Point(self.x//scalar,self.y//scalar)

    def __mod__(self,divisor:'Point') -> 'Point':
        return Point(self.x % divisor.x, self.y % divisor.y)

    def manhattan_distance(self,other:'Point') -> float:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def euclidean_distance(self,other:'Point') -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

    def midpoint(self,other:'Point') -> 'Point':
        return (self + other) / 2

    def get_adjacent_points(self,diagonals:bool=False,
                            lower_bound:Optional['Point']=None,
                            upper_bound:Optional['Point']=None) -> list:
        adj = [Point(0,1),Point(0,-1),Point(1,0),Point(-1,0)]
        if diagonals:
            adj += [Point(1,1),Point(-1,-1),Point(1,-1),Point(-1,1)]
        adj = [self + p for p in adj]
        if lower_bound is not None:
            adj = filter(lambda x: lower_bound <= x, adj)
        if upper_bound is not None:
            adj = filter(lambda x: x < upper_bound, adj)
        return list(adj)

    def in_bounds(self,lower_bound:'Point',upper_bound:'Point') -> bool:
        return lower_bound <= self < upper_bound

    def copy(self) -> 'Point':
        return Point(self.x,self.y)

    def as_tuple(self) -> Tuple[float,float]:
        return (self.x,self.y)

    def is_above(self,other:'Point') -> bool:
        return self.y > other.y

    def is_below(self,other:'Point') -> bool:
        return self.y < other.y

    def is_left_of(self,other:'Point') -> bool:
        return self.x < other.x

    def is_right_of(self,other:'Point') -> bool:
        return self.x > other.x

    def up(self) -> 'Point':
        return self + Point(0,1)

    def down(self) -> 'Point':
        return self + Point(0,-1)

    def left(self) -> 'Point':
        return self + Point(-1,0)

    def right(self) -> 'Point':
        return self + Point(1,0)

    @staticmethod
    def random(lower_bound:'Point',upper_bound:'Point') -> 'Point':
        return Point(randint(lower_bound.x,upper_bound.x),randint(lower_bound.y,upper_bound.y))

ORIGIN: Final[Point] = Point(0,0)
