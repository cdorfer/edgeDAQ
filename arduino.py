#author: dorfer@phys.ethz.ch
import serial
import time
import collections
import numpy as np


class Arduino(object):

    def __init__(self, serial_port='/dev/shutter', baud_rate=9600, read_timeout=5):
        self.conn = serial.Serial(serial_port, baud_rate)
        self.conn.timeout = read_timeout # Timeout for readline()
        time.sleep(0.2)
        print('Connection to Arduino opened.')

        self.temps = collections.deque([20,20,20,20,20],5)

    def open(self, state):
        if state:
            self.conn.write(b'O')
        else:
            self.conn.write(b'C')

    def lightOn(self, state):
        if state:
            self.conn.write(b'L')
        else:
            self.conn.write(b'D')

    def getTemperature(self):
        try:
            self.conn.write(b'T')
            time.sleep(0.001)
            temp = self.conn.readline()
            temp = temp.decode()
            temp = float(temp)
            self.temps.appendleft(temp)
            return temp
        except:
            return 1000 #so we don't overheat our sensor in case something goes wrong, solder will start melting at 270deg
            pass

    def getStoredTemperature(self):
        '''here we just return the class value for the temperature'''
        return round(np.mean(self.temps),2)


    def close(self):
        self.a.close()
        print('Connection to Arduino closed.')