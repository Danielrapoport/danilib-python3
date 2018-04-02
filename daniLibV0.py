# Daniel Rapoport
from abc import *
import random
import math
#Switch (Java) / Case (Ruby)
class Case:
    def __init__(self, x):
        self.x = x
        self.__executed = False
        self.__executable = True
    def __checkRange(self, start, end):
        if end <= start:
            raise Exception()
    def end(self):
        self.__executable = False
    def when(self, val, function):
        if self.x == val or self.x in val and self.__executable:
            function()
            self.__executed = True
    def when_not(self, val, function):
        if self.x != val or self.x not in val and self.__executable:
            function()
            self.__executed = True
    def beetween(self, start, end, function):
        self.__checkRange(start, end)
        if self.x >= start and self.x < end and self.__executable:
            function()
            self.__executed = True
    def out_of(self, start, end, function):
        self.__checkRange(start, end)
        if not (self.x >- start and self.x < end) and self.__executable:
            function()
            self.__executed = True
    def default(self, function):
        if not self.__executed and self.__executable:
            function()
            self.__executed = True
#math Equation classes
#only de [0] of elements is a number, the others are X
#ABSTRACT
class Equation(ABC):
    degree = 1
    elements = [0]
    def __init__(self, elements, exp=1):
        self.degree = len(elements) -1
        self.elements = list(elements)
        self.exp = int(exp)
        super().__init__()
    @abstractmethod
    def solve(self):
        pass
    @abstractmethod
    def getY(self, x):
        pass
    def get_degree(self):
        return self.degree * self.exp

# a*x**exp
class ConstDegree(Equation):
    def __init__(self, elements, exp):
        if len(list(elements)) != 1:
            raise Exception()
        super().__init__(elements, exp)
    @staticmethod
    def copy_init(other):
        return ConstDegree(other.elements, other.exp)
    def solve(self):
        if self.exp == 1:
            return [self.elements[0]]
        else:
            return [self.elements[0] ** self.exp, -self.elements[0] ** self.exp]
    def getY(self, x):
        return self.solve()

# (a*x + b) ** exp
class FirstDegree(Equation):
    def __init__(self, elements, exp=1):
        if len(elements) != 2 or elements[1] == 0:
            raise Exception()
        super().__init__(elements, exp)
    def solve(self):
        solution = [- self.elements[0] / self.elements[1]]
        if self.exp == 1:
            return solution
        else:
            return ConstDegree.copy_init(solution).solve()
    def getY(self, x):
        solution = [self.elements[0] + self.elements[1] * x]
        if self.exp == 1:
            return solution
        else:
            return ConstDegree(solution, self.exp).getY(x)

# f(x) = ax² + bx + c
#Indexes: a=2 b=1 c=0
class SecondDegree(Equation):
    def __init__(self, elements, exp=1):
        if elements[2] == 0:
            raise Exception()
        super().__init__(elements, exp)
    def delta(self):
        return self.elements[1] ** 2 - 4 * self.elements[0] * self.elements[2]
    def bhaskara(self):
        first_element = (-self.elements[1] + self.delta() ** (1/2)) / (2 * self.elements[2])
        second_element = (-self.elements[1] - self.delta() ** (1/2)) / (2 * self.elements[2])
        return [first_element, second_element]
    def solve(self):
        if self.delta() < 0:
            raise Exception() # can't solve with delta lower than zero!
        else:
            return list(map(lambda val: ConstDegree([val], self.exp).solve(), self.bhaskara()))
    def vertex(self):
        # Xv = -b / 2a ; Yv = -Delta / 4a
        vertex = [-self.elements[1]/ (2*self.elements[2]), -self.delta()/(4*self.elements[2])]
        return list(map(lambda val: ConstDegree([val], self.exp).solve(), vertex))
    def in_this_range(self, y):
        if self.elements[2] == 0:
            raise Exception() # Ax² can't be zero!
        elif self.elements[2] < 0:
            if y > self.vertex()[1]:
                return False
        else:
            if y < self.vertex()[1]:
                return False
        return True
    def getY(self, x):
        this_y = self.elements[2] *x**2 + self.elements[1] *x + self.elements[0]
        return ConstDegree([this_y], self.exp).solve()

#list statistics functions
def avg(x):
    return sum(x)/len(x)

def upL(x, val):
    return list(filter(lambda n: n > val, x))

def downL(x, val):
    return list(filter(lambda n: n < val, x))

def upQ(x, val):
    return len(upL(x, val))

def dowQ(x, val):
    return len(downL(x, val))

def upAvgL(x):
    return upL(x, avg(x))

def downAvgL(x):
    return downL(x, avg(x))

def countedList(x):
    pass #HERE

#list math functions
def sum_if(x, function):
    total = 0
    for el in list(x):
        if function(el):
            total += el
    return total

def count_val(x, val):
    quantity = 0
    for el in x:
        if el == val:
            quantity +=1
    return quantity
#lists generators
def genListRandom(size, limit):
    rL = []
    for index in range(size):
        rL.append(random.randint(0, limit))
    return rL

def fillWith(val, size):
    return list(map(lambda x: val, range(size)))

#LOGARITHIM
def log_x(base, val):
    return val ** (1/base)

def log_10(x):
    return log_x(10, x)
#math factorision
is_multiple = lambda x, v: x % v == 0

def is_Prime(x):
    if x <= 0:
        raise Exception()
    if x == 1:
        return True
    for el in range(2, x):
        if is_multiple(x, el):
            return False
    return True

def factorise(x):
    if is_Prime(x):
        return str(x)
    rs =''
    if x < 0:
        rs += '-'
        x = -x
    if x == 0:
        return '0'
    for el in range(2,x):
        if is_multiple(x, el) and is_Prime(el):
            value = int(log_x(el, x))
            if value == 1:
                rs += str(el) + ' '
            else:
                rs += str(el) + '^' + str(value) + ' '
                x /= value
            del value
    return rs
