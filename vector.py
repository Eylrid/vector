import math
from numbers import Number

class DimensionError(Exception):
    pass

class Vector(tuple):
    def __new__(cls, components):
        if any([not isinstance(i, Number) for i in components]):
            raise TypeError('Vector components must be numbers')
        item = tuple.__new__(cls, components)
        item.dimensions = len(item)
        item.length = math.sqrt(sum([i**2 for i in item]))
        return item

    def __getitem__(self, *args):
        result = tuple.__getitem__(self, *args)
        if isinstance(result, tuple):
            result = Vector(result)
        return result

    def __getslice__(self, *args):
        return self.__getitem__(slice(*args))

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
        return math.acos(self.dot(other)/(self.length*other.length))

    def component_along(self, other):
        '''Return the component of self along other'''
        self.check_other(other, 'component_along')
        return self.dot(other)/other.length

    def check_other(self, other, operation):
        '''Raise an error if other is not a compatible vector'''
        if not isinstance(other, Vector):
            raise TypeError("unsupported operand type(s) for %s: 'Vector' and '%s'" %(operation, type(other).__name__))
        if self.dimensions != other.dimensions:
            raise DimensionError('vectors are of different dimensions')

    def direction(self):
        '''Returns a new unit vector with the same direction as self'''
        length = self.length
        components = [i/length for i in self]
        return Vector(components)


class Matrix(tuple):
    def __new__(cls, vectors):
        if any([not isinstance(i, Vector) for i in vectors]):
            raise TypeError('Matrix components must be vectors')
        height = vectors[0].dimensions
        if any([i.dimensions != height  for i in vectors]):
            raise DimensionError('Vectors of different dimensions')
        item = tuple.__new__(cls, vectors)
        item.height = height
        item.width = len(item)
        return item

    def __getitem__(self, *args):
        result = tuple.__getitem__(self, *args)
        if not isinstance(result, Vector):
            try:
                result = Matrix(result)
            except TypeError:
                pass
        return result

    def __getslice__(self, *args):
        return self.__getitem__(slice(*args))
