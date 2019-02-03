import serial
import time

class LowVoltage(object):
	def __init__(self, addr):
		self.lv = serial.Serial(addr, 9600)
		time.sleep(0.2)
		self.initialize()
		self.enabled = False

	def initialize(self):
		self.lv.write(b'*IDN?\r\n') 
		val = self.lv.readline().decode()
		if not val:
			print('Could not connect to low voltage supply!')
			return
		print('Connection to low voltage supply opened.')
		self.lv.write(b'OP2 0\r\n') #turn channel 1 off
		self.lv.write(b'V2 3.9\r\n') #sets voltage
		self.lv.write(b'I2 0.002\r\n') #sets current limit
		self.lv.write(b'OCP2 3\r\n') #current protection trip point


	def turnChannelOn():
		if self.enabled == False:
			self.lv.write(b'OP2 1\r\n') #turn channel 1 on

	def setCurrent(self, curr):
		self.turnChannelOn()
		cmd = 'I2 {}\r\n'.format(curr)
		self.lv.write(cmd.encode()) #changes the current limit
	
	def close(self):
		self.lv.close()
		print('Connection to low voltage supply closed')

	def turnLedOn(self):
		try:
			cmd = 'I2 {}\r\n'.format(0.25)
			self.lv.write(cmd.encode()) #changes the current limit
			self.lv.write(b'OP2 1\r\n')
		except:
			pass

	def turnLedOff(self):
		try:	
			self.lv.write(b'OP2 0\r\n')
		except:
			pass