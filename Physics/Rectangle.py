import Physics.Polygon
import Functions

from Fractals.Point import Point

class Rectangle(Physics.Polygon):
	def __init__(self, points):
		points.insert(1, Point(points[0].x, points[1].y))
		points.insert(3, Point(points[2].x, points[0].y))

		super(Rectangle, self).__init__(points)
		self.drawn = None

	def draw(self, canvas):
		if not self.drawn:
			self.drawn = canvas.create_polygon(self.getBbox(), fill = Functions.makeHexColor(self.color))
			self.tooltip = canvas.create_text(self.getBbox()[:2], fill = "red")
			canvas.tag_bind(self.drawn, '<Button-1>', self.toggleToolTip)
		else:
			canvas.coords(self.drawn, self.getBbox())
			canvas.coords(self.tooltip, self.getBbox()[:2])
			canvas.itemconfig(self.tooltip, state = "normal" if self.ttState else "hidden",
				text = "L{} R{} T{} B{}".format(self.pointl.x, self.pointr.x, self.pointt.y, self.pointb.y))
