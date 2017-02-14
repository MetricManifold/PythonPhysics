
from math import sqrt

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def getPoint(self):
		return self.x, self.y

	def getNormal(self):
		return Point(self.y, -self.x)

	def getMagnitude(self):
		return sqrt(self.x ** 2 + self.y ** 2)

	def getUnit(self):
		m = self.getMagnitude()
		return Point(self.x / m, self.y / m)

	def getDirection(self):
		v = Fractals.Vector.Vector(Fractals.Point.Point(0, 0), self)
		return v.getDirection()

	def isParallel(self, other):
		return self.getDirection() == other.getDirection()

	def __mul__(self, other):
		if (type(other) is Point):
			return self.x * other.x + self.y * other.y
		else:
			return Point(self.x * other, self.y * other)

	def __str__(self):
		return "X:" + str(self.x) + " Y:" + str(self.y)

	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Point(self.x - other.x, self.y - other.y)
