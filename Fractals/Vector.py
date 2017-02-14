from Fractals.Point import *
from math import *

class Vector(object):
	def __init__(self, start, end):
		try:
			self.start = Point(start[0], start[1])
			self.end = Point(end[0], end[1])
		except Exception:
			try:
				self.start = start
				self.end = end
			except Exception as e:
				raise e

	def getDirection(self):
		x = self.end.x - self.start.x
		y = self.start.y - self.end.y

		if x == 0:
			return pi / 2 if y > 0 else 3 * pi / 2
		elif x < 0: 
			return pi + atan(y / x)
		elif y < 0:
			return atan(y / x) + 2 * pi
		else:
			return atan(y / x)

	def getMagnitude(self):
		return sqrt((self.start.x - self.end.x) ** 2 + (self.start.y - self.end.y) ** 2)

	def getLine(self):
		return self.start.x, self.start.y, self.end.x, self.end.y