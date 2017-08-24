import Physics.Rectangle
import Functions

from Fractals.Point import Point

class Player(Physics.Rectangle):
	def __init__(self, points):
		super(Player, self).__init__(points)
