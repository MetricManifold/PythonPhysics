
import time
import Fractals

class PhysicsUpdate(object):
	TICK_INTERVAL = 10 # milliseconds
	PAUSE = False

	def __init__(self, root, canvas):
		self.root = root
		self.canvas = canvas
		self.entities = []
		self.tickLength = 5

		self.doUpdate()

	def doUpdate(self):
		start = time.time()

		for e in self.entities:
			if (not PhysicsUpdate.PAUSE):
				e.update()
			e.draw(self.canvas)

		if (not PhysicsUpdate.PAUSE):
			pairs = self.sweepAndPrune()
			for p in pairs:
				self.doCollisionCheck(*p)


		end = time.time()
		self.root.after(int(PhysicsUpdate.TICK_INTERVAL + start - end), self.doUpdate)

	def addObjects(self, *objects):
		for o in objects:
			self.entities.append(o)
			o.draw(self.canvas)

	def removeObject(self, o):
		self.entities.remove(o)

	def sweepAndPrune(self):
		checkPairs = set()

		# order all entities using insertion sort
		for i in range(1, len(self.entities)):
			j = i
			while (j > 0) and (self.entities[j].pointl.x < self.entities[j - 1].pointl.x):
				self.entities[j], self.entities[j - 1] = self.entities[j - 1], self.entities[j]
				j -= 1

		# check for collisions along x
		intlist = []
		for e in self.entities:
			for i in intlist[:]:
				if i.pointr.x > e.pointl.x:
					if (i.pointt.y < e.pointb.y < i.pointb.y) or (e.pointt.y < i.pointb.y < e.pointb.y):
						checkPairs.add((i, e))
				else:
					intlist.remove(i)
			intlist.append(e)

		return checkPairs

	def doCollisionCheck(self, o1, o2):
		if (o1.type == "polygon" and o2.type == "polygon"):
			self.separatingAxis(o1, o2)
		elif (o1.type == "polygon" and o2.type == "ellipse"):
			self.polyEllipseCheck(o1, o2)
		elif (o1.type == "ellipse" and o2.type == "polygon"):
			self.polyEllipseCheck(o2, o1)
		elif (o1.type == "ellipse" and o2.type == "ellipse"):
			self.ellipseCheck(o2, o1)
		else:
			raise Exception("incorrect object type for collision")

	def polyEllipseCheck(self, poly, ellipse):
		return None

	def ellipseCheck(self, o1, o2):
		return None

	def separatingAxis(self, o1, o2):
		mvt = None

		if (o1.cachedNormal and o1.cachedNormal is o2.cachedNormal):
			res = self._checkNormalSAT(o1.cachedNormal, o1, o2)
			if (not res): return False

		for n in o1.normals + o2.normals:
			res = self._checkNormalSAT(n, o1, o2)
			if (not res):
				o1.cachedNormal = n
				o2.cachedNormal = n
				return False
			else:
				if (not mvt or res.getMagnitude() < mvt.getMagnitude()): 
					mvt = res
		
		return mvt

	def _checkNormalSAT(self, normal, o1, o2):
		bp1, sp1 = self._getProjectionSAT(normal, o1)
		bp2, sp2 = self._getProjectionSAT(normal, o2)
		overlap = max(sp2 - bp1, sp1 - bp2)
			
		if overlap >= 0:
			return None
		else:
			return normal * -overlap

	def _getProjectionSAT(self, normal, check):
		proj = [normal * x for x in check.hull]
		return max(proj), min(proj)

	@classmethod
	def pause(self, event = None):
		PhysicsUpdate.PAUSE = not PhysicsUpdate.PAUSE





