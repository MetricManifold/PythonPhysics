import Physics.PhysicsObject
import Functions
import Fractals
from math import *

class Ellipse(Physics.PhysicsObject):
	def __init__(self, points):
		points.insert(1, Fractals.Point(points[1].x, points[0].y))
		points.insert(3, Fractals.Point(points[0].x, points[2].y))

		super(Ellipse, self).__init__(points)
		self.type = "ellipse"
		self.drawn = None

		self.a = (self.pointr.x - self.pointl.x) / 2
		self.b = (self.pointb.y - self.pointt.y) / 2
		
		self.updateEllipseBox()

	def shiftRotation(self, shift):
		super(Ellipse, self).shiftRotation(shift)
		self.updateEllipseBox()

	def shiftPosition(self, shift):
		super(Ellipse, self).shiftPosition(shift)
		self.updateEllipseBox()

	def updateEllipseBox(self):
		self.ellipseBox = []
		cx, cy = self.getCenter()
		steps = 8

		# create the oval as a list of points
		for i in range(0, steps):
			# Calculate the angle for this step
			theta = float(i) / steps * (2 * pi)

			x1 = self.a * cos(theta)
			y1 = self.b * sin(theta)

			# rotate x, y
			x = (x1 * cos(self.rotation)) - (y1 * sin(self.rotation))
			y = (y1 * cos(self.rotation)) + (x1 * sin(self.rotation))
			
			self.ellipseBox.append(int(x + cx))
			self.ellipseBox.append(int(y + cy))

	def draw(self, canvas):
		if not self.drawn: self.drawn = canvas.create_polygon(self.ellipseBox, fill = Functions.makeHexColor(self.color), smooth = "true")
		else: canvas.coords(self.drawn, self.ellipseBox)

	def pointsFromLine(self, normal):
		return None

	def pointsFromLine(self, line):
		c = Fractals.Point(*self.getCenter())
		t = line.getDirection() - self.rotation
		m = tan(t)
		dx = 1 / sqrt(1 / self.a ** 2 + (m ** 2 * self.b ** 2) / self.a ** 4)
		dy = sqrt(self.b ** 2 - self.b ** 2 / self.a ** 2 * dx ** 2)

		p1 = Fractals.Point(-dx, -dy if m > 0 else dy)
		p2 = Fractals.Point(dx, dy if m > 0 else -dy)

		v = Fractals.Point(dx, dy)
		l = v.getMagnitude()
		r1 = v.getDirection() + self.rotation
		r2 = r1 + pi
			
		p1.x = c.x + l * cos(r1)
		p1.y = c.y - l * sin(r1)
		p2.x = c.x + l * cos(r2)
		p2.y = c.y - l * sin(r2)

		return p1, p2


