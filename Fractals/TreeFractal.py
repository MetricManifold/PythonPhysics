
from tkinter import *
from math import *
import random

from Functions import *
from Fractals.Vector import *

class TreeFractal(object):
	class TreeVector(Vector):
		def getExtension(self, magnitude, direction):
			newEnd = Point(self.end.x + magnitude * cos(direction), self.end.y - magnitude * sin(direction))
			return TreeFractal.TreeVector(self.end, newEnd)

	def __init__(self, canvas):
		self.canvas = canvas
		self.lineArray = []
		self.vLineArray = []

	def _generateTreeFractal(self):
		extendArray = self.lineArray.copy()

		while extendArray:
			root = extendArray.pop()
			if root.getMagnitude() < 10:
				continue

			b1 = root.getExtension(root.getMagnitude() / 2, root.getDirection() + random.uniform(pi / 3, pi / 6))
			b2 = root.getExtension(root.getMagnitude() / 2, root.getDirection() - random.uniform(pi / 3, pi / 6))
			b3 = root.getExtension(root.getMagnitude() / 2, root.getDirection() + random.uniform(-pi / 10, pi / 10))

			self.lineArray.append(b1)
			self.lineArray.append(b2)
			self.lineArray.append(b3)
			extendArray.append(b1)
			extendArray.append(b2)
			extendArray.append(b3)

		print("tree creation complete with", len(self.lineArray), "lines")

	def drawTreeFractal(self, lineArray):
		self.lineArray = lineArray
		self._generateTreeFractal()

		for l in self.lineArray:
			color = makeHexColor(0X4F1900)
			self.vLineArray.append(self.canvas.create_line(l.getLine(), fill = color, width = l.getMagnitude() / 10))

		print("drew", len(self.lineArray), "lines")

	def clearTreeFractal(self):
		for l in self.vLineArray:
			self.canvas.delete(l)
		

