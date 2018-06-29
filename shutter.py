#author: dorfer@phys.ethz.ch
import serial
import time


class Shutter(object):

    def __init__(self, serial_port='/dev/shutter', baud_rate=9600, read_timeout=5):
        self.conn = serial.Serial(serial_port, baud_rate)
        self.conn.timeout = read_timeout # Timeout for readline()
        time.sleep(1)
        print('Connection to Arduino opened.')

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
            ret = self.conn.readline()
            ret = ret.decode()
            return float(ret)
        except:
            return 0
            pass


    def close(self):
        self.a.close()
        print('Connection to Arduino closed.')


