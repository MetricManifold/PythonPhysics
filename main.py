
from tkinter import *
from WindowWorld import *
from WindowFractal import *
from Physics import *
from math import *
import time

from Physics import *
from Fractals import *


def main():
	master = Tk()
	doPhysics(master)
	master.mainloop()


def doPhysics(master):
	window = WindowWorld(master)


def doFractals(master):
	window = WindowFractal(master)

	c = RecursiveCircle(window.canvas)
	k = KochCurve(window.canvas)
	t = TreeFractal(window.canvas)

	radius = 200
	lineArray1 = [
		k.KochVector(Point(window.width / 3, 2 * window.height / 3), Point(window.width / 2, window.height / 3)),
		k.KochVector(Point(window.width / 2, window.height / 3), Point(2 * window.width / 3, 2 * window.height / 3)),
		k.KochVector(Point(2 * window.width / 3, 2 * window.height / 3), Point(window.width / 3, 2 * window.height / 3))
		]
	lineArray2 = [
		t.TreeVector(Point(window.width / 2, window.height), Point(window.width / 2, window.height / 2))
		]

	#c.drawCircleInset(window.height / 2, window.width / 2, radius)
	#k.drawKochCurve(lineArray1)
	#t.drawTreeFractal(lineArray2)


if __name__ == '__main__':
	main()