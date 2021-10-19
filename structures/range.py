from typing import Iterable, Union


class Range:
    def __init__(self,lower:Union[int,float],
                 upper:Union[int,float],
                 lower_inclusive:bool=True,
                 upper_inclusive:bool=False):
        self.lower = lower
        self.lower_inclusive = lower_inclusive

        self.upper = upper
        self.upper_inclusive = upper_inclusive

    def size(self) -> Union[int,float]:
        offset = (1 if self.lower_inclusive else 0) + (1 if self.upper_inclusive else 0) - 1
        return self.upper - self.lower + offset

    def __len__(self) -> Union[int,float]:
        return self.size()

    def __lt__(self,other) -> bool:
        return self.lower < other.lower

    def __gt__(self,other) -> bool:
        return self.lower > other.lower

    def __str__(self) -> str:
        lchar = '[' if self.lower_inclusive else '('
        rchar = ']' if self.upper_inclusive else ')'
        return f'{lchar}{self.lower}-{self.upper}{rchar}'

    def __contains__(self,item) -> bool:
        if self.lower_inclusive:
            if self.upper_inclusive:
                return self.lower <= item <= self.upper
            return self.lower <= item < self.upper

        if self.upper_inclusive:
            return self.lower < item <= self.upper
        return self.lower < item < self.upper

    @staticmethod
    def from_string(string,lower_inclusive:bool=True,upper_inclusive:bool=False) -> 'Range':
        split = string.split('-')
        l,r = int(split[0]),int(split[1])
        return Range(l,r,lower_inclusive,upper_inclusive)

    def division(self,parts:int,which:int) -> 'Range':
        # if self.size() % parts:
        #     raise ValueError(f'Range should be evenly divided, {self.size()} % {parts} != 0')
        if which >= parts:
            raise IndexError('Cannot select a chunk out of range')
        step = (self.upper-self.lower) / parts
        if float(step).is_integer():
            step = int(step)
        lower = self.lower + (step * which)
        upper = lower + step
        return Range(lower,upper)

    def __iter__(self) -> Iterable[Union[int,float]]:
        if not isinstance(self.lower,int):
            raise TypeError(f'\'{type(self.lower)}\' cannot be interpreted as an integer')
        if not isinstance(self.upper,int):
            raise TypeError(f'\'{type(self.upper)}\' cannot be interpreted as an integer')
        lower = self.lower if self.lower_inclusive else self.lower+1
        upper = self.upper+1 if self.upper_inclusive else self.upper
        for i in range(lower,upper):
            yield i
