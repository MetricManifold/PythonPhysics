
from tkinter import *
from math import *
import random

from Fractals.Vector import *
from Functions import *

class KochCurve(object):
	class KochVector(Vector):
		def getSegment(self, start, end):
			if start >= end:
				raise ArithmeticError("start cannot be less than end")

			direction = self.getDirection()
			magnitude = self.getMagnitude()

			newStart = Point(self.start.x + start * magnitude * cos(direction), self.start.y - start * magnitude * sin(direction))
			newEnd = Point(newStart.x + end * magnitude * cos(direction), newStart.y - end * magnitude * sin(direction))

			return KochCurve.KochVector(newStart, newEnd)

	def __init__(self, canvas):
		self.canvas = canvas
		self.lineArray = []
		self.vLineArray = []
		
	def _generateKochCurve(self):
		newLineArray = []

		for l in self.lineArray:
			p1 = l.getSegment(0, 1/3).end
			p2 = self.KochPoint(p1.x + l.getMagnitude() / 3 * cos(l.getDirection() + pi / 3),
				p1.y - l.getMagnitude() / 3 * sin(l.getDirection() + pi / 3))
			p3 = l.getSegment(2/3, 1).start

			newLineArray.append(self.KochVector(l.start, p1))
			newLineArray.append(self.KochVector(p1, p2))
			newLineArray.append(self.KochVector(p2, p3))
			newLineArray.append(self.KochVector(p3, l.end))

		self.lineArray = newLineArray

		if self.lineArray[-1].getMagnitude() < 10: return

		self._generateKochCurve()

	def drawKochCurve(self, lineArray):
		self.lineArray = lineArray
		self._generateKochCurve()

		for l in self.lineArray:
			color = makeHexColor(int(0xFFFFFF * random.random() * 32) % 0xFFFFFF)
			self.vLineArray.append(self.canvas.create_line(l.getLine(), fill = color))

		print("drew", len(self.lineArray), "lines")

