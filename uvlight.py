

class UVLight(object):
	def __init__(self, lv):
		self.lv = lv
		self.status = 0 #off

	def switchLED(self, ctrl):
		if ctrl == 1 and self.status == 0:
			self.lv.turnLedOn()
			self.status = 1
		if ctrl == 0 and self.status == 1:
			self.lv.turnLedOff()
			self.status = 0