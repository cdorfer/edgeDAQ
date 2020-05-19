

class Illumination(object):
	def __init__(self, lv):
		self.lv = lv
		self.statusUV = 0 #off
		self.statusIR = 0

	def switchUVLED(self, ctrl):
		if ctrl == 1 and self.statusUV == 0:
			self.lv.turnUVLedOn()
			self.statusUV = 1
		if ctrl == 0 and self.statusUV == 1:
			self.lv.turnUVLedOff()
			self.statusUV = 0

	def switchIRLED(self, ctrl):
		if ctrl == 1 and self.statusIR == 0:
			self.lv.turnIRLedOn()
			self.statusIR = 1
		if ctrl == 0 and self.statusIR == 1:
			self.lv.turnIRLedOff()
			self.statusIR = 0