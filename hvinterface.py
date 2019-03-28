from pymouse import PyMouse
from pykeyboard import PyKeyboard
from time import sleep


import logging
logger = logging.getLogger('HV-Bot')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('/home/dorfer/controlBot/hvbot.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s : %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


GREEN = '\033[92m'
ENDC = '\033[0m'

#positions without uv light enabled
pos_wo = {	'config_osci':[62,729],
		'new_file':[154,729],
		'collect_wf':[235,729],
		'start_scan':[313,729],
		'stop_scan':[394,729],
		'close_file':[477,729],
		'shutter':[96,769],
		'light_control':[269,769],
		'plotting':[832,774],
		'keithley':[168,936],
		'daq_window':[41,652]}

#positions with UV enabled
pos = {'config_osci':[62,729],
		'new_file':[154,729],
		'collect_wf':[235,729],
		'start_scan':[313,729],
		'stop_scan':[394,729],
		'close_file':[477,729],
		'shutter':[85,769],
		'light_control':[208,769],
		'plotting':[832,774],
		'keithley':[168,936],
		'daq_window':[41,652],
		'uvled':[328,769]}



class HVInterface(object):
	def __init__(self):
		self.m = PyMouse()
		self.k = PyKeyboard()
		self.led = 0 #0=off, 1=on
		self.shutter = 0 #0=off, 1=on
		self.uvled  = 0 #0=off, 1=on
		self.nr = 0

	def clickStuff(self, target, rest=0.5):
		p = pos[target]
		self.m.click(p[0], p[1], 1)
		sleep(rest)

	def setVoltage(self, voltage):
		self.clickStuff('keithley')
		self.k.tap_key(self.k.enter_key)

		logger.info('Set bias voltage to {}V'.format(voltage))
		text = 'BIAS HV6 {}'.format(voltage)
		for letter in text:
			self.k.tap_key(letter)
		self.k.tap_key(self.k.enter_key)


