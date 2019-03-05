#author: dorfer@phys.ethz.ch
import serial
import time
import collections
import numpy as np
import os


class Arduino(object):

    def __init__(self, logger, serial_port='/dev/arduino', baud_rate=9600, read_timeout=0.5):
        self.logger = logger

        self.conn = serial.Serial(serial_port, baud_rate)
        self.conn.timeout = read_timeout # Timeout for readline()
        time.sleep(0.2)
        self.logger.info('Connection to Arduino opened.')

        self.temps = collections.deque([20,20,20,20,20],5)
        self.serial_port = serial_port
        self.baud_rate = baud_rate
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
            if self.getConfirmation():
                return
            else:
                self.write(command)
        except Exception as e:
            self.logger.warning('Exception in arduino.py: write method: {}'.format(e))


    def write_read_float(self, command):
        return -1
        '''
        try:
            self.conn.write(command)
            time.sleep(0.001)
            ret = self.conn.readline()
            ret = ret.decode()
            ret = float(ret)
            return ret
        except Exception as e:
            print('Exception:')
            print(e)
        '''


    def getConfirmation(self):
        try:
            ret = self.conn.readline()
            ret = ret.decode()
            ret = int(ret)
            if ret != 1:
                self.hard_reconnect()
                self.logger.warning('Arduino connection crashed after {} instructions'.format(self.instruction_nr))
                self.instruction_nr = 0
                return False
            else:
                return True
        except Exception as e:
            self.logger.warning('Exception in arduino.py: getConfirmation method: {}'.format(e))
            self.hard_reconnect()
            return False


    def open(self, state):
        if state:
            self.write(b'O')
        else:
            self.write(b'C')


    def lightOn(self, state):
        if state:
            self.write(b'L')
        else:
            self.write(b'D')

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