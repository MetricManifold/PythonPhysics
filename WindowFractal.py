
from tkinter import *
from math import *
from Fractals import *

class WindowFractal(object):
	height = 500
	width = 500

	def __init__(self, master):
		self.canvas = None

		# gui elements for fractals
		self.angleLabel = None
		self.canvasLine = None
		self.pointThird = None
		self.pointTwoThird = None
		self.logicalLine = None
		self.triangleEdge1 = None
		self.triangleEdge2 = None

		# variables
		self.centerSegment = False
		self.angleLabelText = StringVar()
		self.canvasMotionId = None
		self.canvasClickId = None

		self.master = master
		self.k = None
		self.t = None
		self.p = None

		master.title("A Fractal Test")
		master.resizable(0, 0)
		self.setupElements()

	def setupElements(self):
		self.canvas = Canvas(self.master, width = self.width, height = self.height, background = "#C4FFEE")
		self.canvas.pack()
		self.canvasClickId = self.canvas.bind('<Button-1>', self.toggleCenterSegment)

		self.angleLabel = Label(self.master, textvariable = self.angleLabelText, relief = "groove")
		self.angleLabel.pack(fill = "x")

		self.canvasLine = self.canvas.create_line(0, 0, 0, 0)
		self.pointThird = self.canvas.create_oval(0, 0, 0, 0)
		self.pointTwoThird = self.canvas.create_oval(0, 0, 0, 0)
		self.triangleEdge1 = self.canvas.create_line(0, 0, 0, 0)
		self.triangleEdge2 = self.canvas.create_line(0, 0, 0, 0)

		self.k = KochCurve(self.canvas)
		self.t = TreeFractal(self.canvas)

	def toggleCenterSegment(self, event):
		if self.centerSegment:
			self.canvas.unbind('<Motion>', self.canvasMotionId)
			self.centerSegment = False
		else:
			self.canvasMotionId = self.canvas.bind('<Motion>', self.motionTreeLine)
			self.logicalLine = Vector(Point(event.x, event.y), Point(event.x, event.y))
			self.centerSegment = True

	# responds to mouse click and grows koch fractal depending on how far mouse tracks from initial position
	def motionKochLine(self, event):
		newLine = self.k.KochVector(Point(self.logicalLine.start.x, self.logicalLine.start.y), Point(event.x, event.y))
		self.logicalLine = newLine

		# get the third segments
		firstThird = self.logicalLine.getSegment(0, 1/3)
		secondThird = self.logicalLine.getSegment(2/3, 1)
		ellipseRadius = 3

		# line drawing from initial to current position
		self.canvas.coords(self.canvasLine,
			self.logicalLine.start.x, self.logicalLine.start.y, self.logicalLine.end.x, self.logicalLine.end.y)
		# ovals over the third points
		self.canvas.coords(self.pointThird,
			firstThird.end.x - ellipseRadius, firstThird.end.y - ellipseRadius, 
			firstThird.end.x + ellipseRadius, firstThird.end.y + ellipseRadius)
		self.canvas.coords(self.pointTwoThird,
			secondThird.start.x - ellipseRadius, secondThird.start.y - ellipseRadius, 
			secondThird.start.x + ellipseRadius, secondThird.start.y + ellipseRadius)
		# lines creating the triangle in the center third
		self.canvas.coords(self.triangleEdge1,
			firstThird.end.x, firstThird.end.y, firstThird.end.x + firstThird.getMagnitude() * cos(self.logicalLine.getDirection() + pi / 3),
			firstThird.end.y - firstThird.getMagnitude() * sin(self.logicalLine.getDirection() + pi / 3))
		self.canvas.coords(self.triangleEdge2,
			firstThird.end.x + firstThird.getMagnitude() * cos(self.logicalLine.getDirection() + pi / 3),
			firstThird.end.y - firstThird.getMagnitude() * sin(self.logicalLine.getDirection() + pi / 3), secondThird.start.x, secondThird.start.y)

		self.angleLabelText.set('{}, {} @ {}*'.format(event.x, event.y, self.logicalLine.getDirection() * 360 / 2 / pi))

	# responds to mouse click and draws tree depending on how far mouse tracks from initial position
	def motionTreeLine(self, event):
		newLine = self.t.TreeVector(Point(self.logicalLine.start.x, self.logicalLine.start.y), Point(event.x, event.y))
		self.logicalLine = newLine

		self.t.clearTreeFractal()
		self.t.drawTreeFractal([self.logicalLine])

		self.angleLabelText.set('New Tree, start = {}, {} @ {}*'.format(self.logicalLine.start.x, self.logicalLine.start.y, self.logicalLine.getMagnitude() * 2))

