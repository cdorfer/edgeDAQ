import serial
import time

class LowVoltage(object):
	def __init__(self, addr, logger):
		self.addr = addr
		self.logger = logger
		self.open()
		self.initialize()
		self.enabled = False
		

	def open(self):
		self.lv = serial.Serial(self.addr, 9600)
		time.sleep(0.2)
		
	def initialize(self):
		self.lv.write(b'*IDN?\r\n') 
		val = self.lv.readline().decode()
		if not val:
			self.logger.warning('Could not connect to low voltage supply!')
			return
		self.logger.info('Connection to low voltage supply opened.')
		self.lv.write(b'OP2 0\r\n') #turn channel 1 off
		self.lv.write(b'V2 3.9\r\n') #sets voltage
		self.lv.write(b'I2 0.002\r\n') #sets current limit
		self.lv.write(b'OCP2 3\r\n') #current protection trip point


	def turnChannelOn(self):
		if self.enabled == False:
			self.lv.write(b'OP2 1\r\n') #turn channel 1 on

	def setCurrent(self, curr):
		self.turnChannelOn()
		cmd = 'I2 {}\r\n'.format(curr)
		self.lv.write(cmd.encode()) #changes the current limit
	
	def close(self):
		self.lv.close()
		self.logger.info('Connection to low voltage supply closed')


	def turnLedOn(self):
		try:
			cmd = 'I2 {}\r\n'.format(0.25) #0.25
			self.lv.write(cmd.encode()) #changes the current limit
			self.lv.write(b'OP2 1\r\n')
		except Exception as e:
			self.logger.warning('lowvoltage.py: turnLedOn() had an exception: {}'.format(e))
			self.close()
			self.open()
			self.initialize()
			self.turnLedOn()
			pass

	def turnLedOff(self):
		try:
			self.lv.write(b'OP2 0\r\n')
		except:
			self.logger.warning('lowvoltage.py: turnLedOff() had an exception: {}'.format(e))
			self.close()
			self.open()
			self.initialize()
			self.turnLedOff()
			pass