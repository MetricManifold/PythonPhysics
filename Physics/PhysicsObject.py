
from Fractals.Vector import Vector
from Fractals.Point import Point
from math import *
import operator

class PhysicsObject(object):
	def __init__(self, points):
		self.points = points
		self.hull = None
		self.normals = None
		self.velocity = [0, 0]
		self.angularv = 0
		self.rotation = 0

		self.color = 0x000000
		self.moving = False
		self.ttState = False

		self.num = 0
		self.radius = 0
		self.pointl = None
		self.pointr = None
		self.pointb = None
		self.pointt = None

		self.cachedNormal = None

		self.setPointNum()
		self.setRadius()
		self.setLPoint()
		self.setRPoint()
		self.setBPoint()
		self.setTPoint()

		self.quickHull()
		self.getNormals()

	# update this shape
	def update(self):
		if (self.velocity != [0, 0]):	
			self.shiftPosition(self.velocity)
			self.shiftRotation(self.angularv)
			self.setLPoint()
			self.setRPoint()
			self.setBPoint()
			self.setTPoint()	

	def toggleToolTip(self, canvas, event = None):
		self.ttState = not self.ttState

	def shiftPosition(self, shift):
		for b in self.points:
			b.x += shift[0]
			b.y -= shift[1]

	# rotation is defined in a clockwise direction
	def shiftRotation(self, shift):
		self.rotation += shift
		c = Point(*self.getCenter())
		for b in self.points:
			(x, y) = (b.x - c.x, b.y - c.y)
			b.x = (x * cos(shift)) - (y * sin(shift)) + c.x
			b.y = (y * cos(shift)) + (x * sin(shift)) + c.y

	# return the magnitude of the velocity for this shape
	def getSpeed(self):
		return sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)

	# return the geometric center of this chape
	def getCenter(self):
		return sum([b.x for b in self.points]) / self.num, sum([b.y for b in self.points]) / self.num

	# returns the bounding box used for drawing
	def getBbox(self):
		bbox = []
		for b in self.points: bbox += b.getPoint()
		return bbox

	# returns the hull box
	def getHullBbox(self):
		bbox = []
		for b in self.hull: bbox += b.getPoint()
		return bbox

	# creates a variable with the number of points
	def setPointNum(self):
		self.num = len(self.points)

	# compute the largest radius containing this shape
	def setRadius(self):
		cx, cy = self.getCenter()
		for b in self.points:
			dr = sqrt((b.x - cx) ** 2 + (b.y - cy) ** 2)
			if dr > self.radius: self.radius = dr

	# moves the center of this shape to the specified position
	def moveCenter(self, position):
		self.shiftPosition(list(map(operator.sub, position, getCenter())))

	# set the leftmost point
	def setLPoint(self):
		for b in self.points:
			if not self.pointl or b.x < self.pointl.x: 
				self.pointl = b

	# set the rightmost point
	def setRPoint(self):
		for b in self.points:
			if not self.pointr or b.x > self.pointr.x: 
				self.pointr = b

	# set the topmost point
	def setTPoint(self):
		for b in self.points:
			if not self.pointt or b.y < self.pointt.y: 
				self.pointt = b

	# set bottommost point
	def setBPoint(self):
		for b in self.points:
			if not self.pointb or b.y > self.pointb.y:
				self.pointb = b

	# form an array of normals to edges
	def getNormals(self):
		self.normals = []
		for i in range(1, len(self.hull)):
			p1 = self.hull[i - 1]
			p2 = self.hull[i]
			self.normals.append((p2 - p1).getNormal().getUnit())

	# form a convex hull around this shape
	def quickHull(self):
		self.hull = [self.pointl, self.pointr]

		dtheta = 2 * pi - Vector(self.pointl, self.pointr).getDirection()
		up = [x for x in self.points
			if x not in self.hull 
			and 0 < (Vector(self.pointl, x).getDirection() + dtheta) % (2 * pi) <= pi]
		down = [x for x in self.points
			if x not in self.hull
			and pi <= (Vector(self.pointl, x).getDirection() + dtheta) % (2 * pi) < 2 * pi]

		self._findHull(up, self.pointl, self.pointr)
		self._findHull(down, self.pointr, self.pointl)

		cx, cy = self.getCenter()

		up = [x for x in self.hull if x.y < cy]
		down = [x for x in self.hull if x.y >= cy]

		# order all points in drawing order
		for i in range(1, len(down)):
			j = i
			while (j > 0) and (down[j].x > down[j - 1].x):
				down[j], down[j - 1] = down[j - 1], down[j]
				j -= 1
		for i in range(1, len(up)):
			j = i
			while (j > 0) and (up[j].x < up[j - 1].x):
				up[j], up[j - 1] = up[j - 1], up[j]
				j -= 1

		self.hull = up + down

	def _findHull(self, points, a, b):
		if len(points) == 0:
			return

		farP = None
		dist = 0
		v = b - a

		# projection
		for p in points:
			rej = (p - a) - v * (((p - a) * v) / (v * v))
			newdist = rej.getMagnitude()

			if not farP or newdist > dist:
				farP = p
				dist = newdist

		self.hull.append(farP)

		dtheta1 = 2 * pi - Vector(a, farP).getDirection()
		dtheta2 = 2 * pi - Vector(farP, b).getDirection()
		left = [x for x in points 
			if x not in self.hull
			and 0 < (Vector(a, x).getDirection() + dtheta1) % (2 * pi) <= pi]
		right = [x for x in points 
			if x not in self.hull
			and 0 < (Vector(farP, x).getDirection() + dtheta2) % (2 * pi) <= pi]

		self._findHull(left, a, farP)
		self._findHull(right, farP, b)


