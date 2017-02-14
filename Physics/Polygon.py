import Physics.PhysicsObject
import Functions

class Polygon(Physics.PhysicsObject):
	def __init__(self, points):
		super(Polygon, self).__init__(points)
		self.type = "polygon"
		self.drawn = None

	def draw(self, canvas):
		if not self.drawn:
			self.drawn = canvas.create_polygon(self.getBbox(), fill = Functions.makeHexColor(self.color))
		else:
			canvas.coords(self.drawn, self.getBbox())


