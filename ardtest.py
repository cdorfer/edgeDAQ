from arduino import Arduino
from time import sleep
import logging
import sys
from datetime import datetime

logger = logging.getLogger('ArduinoTest')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('ardTest.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s : %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


def main():
	ard = Arduino(logger, serial_port='/dev/arduino')
	while True:
		ard.fireNDelayedShots(20)
		#ard.openShutter(True)
		sleep(2)

if __name__ == '__main__':
	main()