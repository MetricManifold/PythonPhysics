
from tkinter import *
from math import *
from Physics import *
from Fractals.Point import Point

class WindowWorld(object):
	height = 500
	width = 500

	# a structure for common object dimensions
	class Dims(object):
		squarex = 20
		squarey = 20
		rectanglex = 30
		rectangley = 10
		staroutr = 20
		starinr = 8

		posx = 100
		posy = 100

		@classmethod
		def getbboxSquare(self, shift = Point(0, 0)):
			return [Point(self.posx, self.posy) + shift, Point(self.posx + self.squarex, self.posy + self.squarey) + shift]

		@classmethod
		def getbboxRectangle(self, shift = Point(0, 0)):
			return [Point(self.posx, self.posy) + shift, Point(self.posx + self.rectanglex, self.posy + self.rectangley) + shift]

		@classmethod
		def getbboxStar(self, shift = Point(0, 0)):
			points = []
			pokes = 5
			for i in range(0, pokes * 2):
				if (i % 2 == 0):
					x = self.posx + self.staroutr * cos(2 * pi / pokes * i)
					y = self.posy - self.staroutr * sin(2 * pi / pokes * i)
				else:
					x = self.posx + self.starinr * cos(2 * pi / pokes * i + (pi / pokes))
					y = self.posy - self.starinr * sin(2 * pi / pokes * i + (pi / pokes))
				points += [Point(x, y)]
			return points

	def __init__(self, master):
		self.canvas = None
		self.physics = None
		self.master = master

		# variables
		self.mySquare = None
		self.myRect = None

		self.master.title("A Fractal Test")
		self.master.resizable(0, 0)
		self.setupElements()

		self.master.bind("<space>", PhysicsUpdate.pause)

	def setupElements(self):
		self.canvas = Canvas(self.master, width = self.width, height = self.height, background = "#C4FFEE")
		self.canvas.pack()

		self.physics = PhysicsUpdate(self.master, self.canvas)

		self.mySquare = Rectangle(WindowWorld.Dims.getbboxSquare())
		self.mySquare.velocity = [0.0, 0.0] # travels southeast

		self.myRect = Rectangle(WindowWorld.Dims.getbboxSquare())
		self.myRect.velocity = [0, -0.5] # travels south

		self.myRect2 = Rectangle(WindowWorld.Dims.getbboxSquare())
		self.myRect2.velocity = [1.0, 0.0] # travels east

		self.myRect3 = Rectangle(WindowWorld.Dims.getbboxSquare(Point(WindowWorld.Dims.squarex / 2, WindowWorld.Dims.squarex / 2)))
		self.myRect3.velocity = [1.0, 0.0] # travels east

		self.myStar = Polygon(WindowWorld.Dims.getbboxStar())
		self.myStar.velocity = [0.1, 0.1]
		self.myStar.angularv = 0.04

		self.physics.addObjects(self.mySquare, self.myRect, self.myRect2, self.myRect3, self.myStar)



