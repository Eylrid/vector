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

    def __getitem__(self, index, *args, **kwargs):
        if isinstance(index, int):
            #integer index, return vector
            return tuple.__getitem__(self, index, *args, **kwargs)
        elif isinstance(index, slice):
            #slice index, return matrix
            return Matrix(tuple.__getitem__(self, index, *args, **kwargs))
        elif isinstance(index, tuple):
            #multidimensional index or slice, slice matrix and vectors
            if len(index) != 2:
                raise DimensionError('multidimensional slicing of Matrix only supports 2 dimensional slicing')

            xindex = index[0]
            yindex = index[1]
            if isinstance(xindex, int):
                return self[xindex][yindex]
            elif isinstance(xindex, slice):
                if isinstance(yindex, int):
                    return Vector([i[yindex] for i in self[xindex]])
                elif isinstance(yindex, slice):
                    return Matrix([i[yindex] for i in self[xindex]])
                else:
                    raise TypeError('invalid index type')
            else:
                raise TypeError('invalid index type')
        else:
            raise TypeError('invalid index type')

    def __getslice__(self, *args, **kwargs):
        return self.__getitem__(slice(*args, **kwargs))


class SquareMatrix(Matrix):
    def __new__(cls, vectors):
        item = Matrix.__new__(cls, vectors)
        if item.width != item.height:
            raise DimensionError('matrix not square')
        item.size = item.width
        return item

    def determinant(self):
        if self.size == 1:
            return self[0,0]
        else:
            determinant = 0
            bottom = self[1:]
            for i, entry in enumerate(self[0]):
                if entry == 0: continue #Term is 0. Cofactor does not matter.
                cofactor = self.cofactor(0, i)
                determinant += entry * cofactor

            return determinant

    def cofactor(self, x, y):
        sign = self.sign(x,y)
        minor = self.minor(x,y)
        return sign*minor

    def sign(self, x, y):
        return (-1)**(x+y)

    def minor(self, x, y):
        vectors = []
        for i, vector in enumerate(self):
            if i == x: continue #Vector being removed
            vector = Vector(tuple(vector[:y])+tuple(vector[y+1:]))
            vectors.append(vector)
        return SquareMatrix(vectors).determinant()
