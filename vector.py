import math

class Vector:
    def __init__(self, components):
        self.components = components

    def __repr__(self):
        return '<' + ', '.join([str(i) for i in self.components]) + '>'

    def __add__(self, other):
        '''Adds self and other and returns a new vector'''
        self.check_other(other, '+')
        components = [a+b for a,b in zip(self.components, other.components)]
        return Vector(components)

    def __sub__(self, other):
        '''Subtracts other from self and returns a new vector'''
        self.check_other(other, '-')
        components = [a-b for a,b in zip(self.components, other.components)]
        return Vector(components)

    def __mul__(self, scalar):
        '''Multiples the vector by scalar and returns a new vector'''
        components = [a*scalar for a in self.components]
        return Vector(components)

    def __div__(self, scalar):
        '''Divides the vector by scalar and returns a new vector'''
        components = [a/scalar for a in self.components]
        return Vector(components)

    def check_other(self, other, operation):
        '''Raise an error if other is not a compatible vector'''
        if not isinstance(other, Vector):
            raise TypeError("unsupported operand type(s) for %s: 'Vector' and '%s'" %(operation, type(other).__name__))
        if self.dimensions() != other.dimensions():
            raise ValueError('vectors are of different dimensions')

    def dimensions(self):
        '''Returns the number of dimensions the vector is defined for'''
        return len(self.components)

    def length(self):
        '''Returns the length of the vector'''
        return math.sqrt(sum([i**2 for i in self.components]))

    def direction(self):
        '''Returns a new unit vector with the same direction as self'''
        length = self.length()
        components = [i/length for i in self.components]
        return Vector(components)
