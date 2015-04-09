import math

class Vector(tuple):
    def __new__(cls, components):
        return tuple.__new__(cls, components)

    def __repr__(self):
        return '<' + ', '.join([str(i) for i in self]) + '>'

    def __add__(self, other):
        '''Adds self and other and returns a new vector'''
        self.check_other(other, '+')
        components = [a+b for a,b in zip(self, other)]
        return Vector(components)

    def __sub__(self, other):
        '''Subtracts other from self and returns a new vector'''
        self.check_other(other, '-')
        components = [a-b for a,b in zip(self, other)]
        return Vector(components)

    def __mul__(self, scalar):
        '''Multiples the vector by scalar and returns a new vector'''
        components = [a*scalar for a in self]
        return Vector(components)

    def __div__(self, scalar):
        '''Divides the vector by scalar and returns a new vector'''
        components = [a/scalar for a in self]
        return Vector(components)

    def dot(self, other):
        '''Return the dot product of self and other'''
        self.check_other(other, 'dot')
        return sum([a*b for a,b in zip(self, other)])

    def orthogonal(self, other):
        '''Return True if self and other are orthogonal'''
        self.check_other(other, 'orthogonal')
        return self.dot(other) == 0

    def angle(self, other):
        '''Return the angle between self and other'''
        self.check_other(other, 'angle')
        return math.acos(self.dot(other)/(self.length()*other.length()))

    def component_along(self, other):
        '''Return the component of self along other'''
        self.check_other(other, 'component_along')
        return self.dot(other)/other.length()

    def check_other(self, other, operation):
        '''Raise an error if other is not a compatible vector'''
        if not isinstance(other, Vector):
            raise TypeError("unsupported operand type(s) for %s: 'Vector' and '%s'" %(operation, type(other).__name__))
        if self.dimensions() != other.dimensions():
            raise ValueError('vectors are of different dimensions')

    def dimensions(self):
        '''Returns the number of dimensions the vector is defined for'''
        return len(self)

    def length(self):
        '''Returns the length of the vector'''
        return math.sqrt(sum([i**2 for i in self]))

    def direction(self):
        '''Returns a new unit vector with the same direction as self'''
        length = self.length()
        components = [i/length for i in self]
        return Vector(components)
