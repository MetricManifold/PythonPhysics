
from tkinter import *
from Functions import *
import random

class RecursiveCircle(object):

	def __init__(self, canvas):
		self.canvas = canvas
		self.circles = []

	def drawCircleInset(self, x, y, radius):
		while radius > 2:
			bbox = [x - radius, y - radius, x + radius, y + radius]
			color = makeHexColor(int(0xFFFFFF * random.random() * radius) % 0xFFFFFF)
			self.circles.append((bbox, color))
			radius *= 0.75
		
		print("circle inset complete with", len(self.circles), "circles")
		self._drawArray()

	def drawCircleHorizon(self, x, y, radius):
		circleStack = [(x, radius)]

		while circleStack:
			(x, radius) = circleStack.pop()

			if x > canvas.winfo_width() or x + radius < 0: continue

			bbox = [x - radius, y - radius, x + radius, y + radius]
			color = makeHexColor(int(0xFFFFFF * random.random() * radius) % 0xFFFFFF)
			self.circles.append((bbox, color))

			if radius > 4: 
				circleStack.append((x - radius, radius * 0.75))
				circleStack.append((x + radius, radius * 0.75))

		print("circle horizon complete with", len(self.circles), "circles")
		self._drawArray()

	def _drawArray(self):
		for c in self.circles:
			self.canvas.create_oval(c[0], outline = c[1])
		print("drew", len(self.circles), "circles")


