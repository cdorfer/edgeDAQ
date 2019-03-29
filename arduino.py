#author: dorfer@phys.ethz.ch
import serial
import time
import collections
import numpy as np
import os
from time import sleep


class Arduino(object):

    def __init__(self, logger, serial_port='/dev/arduino', baud_rate=115200, read_timeout=0.5):
        self.logger = logger

        #open connection
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.conn = serial.Serial(serial_port, baud_rate)
        self.conn.timeout = read_timeout #Timeout for readline()
        
        time.sleep(0.2)
        self.logger.info('Connection to Arduino opened.')

        self.temps = collections.deque([20,20,20,20,20],5)
        self.instruction_nr = 0

    def hard_reconnect(self):
        self.logger.warning('Doing a hard reconnect of the Arduino serial connection.')
        os.system('sudo /home/dorfer/scripts/reconnect_usb.sh')
        time.sleep(1)
        self.conn = serial.Serial(self.serial_port, self.baud_rate)
        time.sleep(0.2)
        self.logger.warning('Did a hard reconnect of the Arduino serial connection.')

    def write(self, command):
        try:
            self.conn.write(command)
            self.instruction_nr += 1
        except Exception as e:
            self.logger.warning('Exception in arduino.py: write method: {}'.format(e))
            self.hard_reconnect()
            sleep(1)
            self.write(command)

    def openShutter(self, state):
        if state:
            self.write(b'O')
            self.logger.info('Opening shutter.')
        else:
            self.write(b'C')
            self.logger.info('Closing shutter.')


    def lightOn(self, state):
        if state:
            self.write(b'L')
            self.logger.info('Turning white LED on.')
        else:
            self.write(b'F')
            self.logger.info('Turning white LED off.')

    def fireNShots(self, nr):
        unicode_str = 'N {}'.format(nr)
        byte_str = unicode_str.encode()
        self.write(byte_str)
        self.logger.info('Fired {} shots.'.format(nr))  

    def fireNDelayedShots(self, nr):
        unicode_str = 'D {}'.format(nr)
        byte_str = unicode_str.encode()
        self.write(byte_str)
        self.logger.info('Fired {} delayed shots.'.format(nr))     

    def write_read_float(self, command):
        return -1 #needed for temp readout in the future

    def getTemperature(self):
        try:
            #temp = self.write_read_float(b'T')
            temp = 1000
        except:
            temp = 1000
            pass

        self.temps.appendleft(temp)
        return temp

    def getStoredTemperature(self):
        '''here we just return the class value for the temperature'''
        return round(np.mean(self.temps),2)


    def close(self):
        self.conn.close()
        self.logger.info('Connection to Arduino closed.')