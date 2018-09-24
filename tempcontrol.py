import sys
import serial
import time
from simple_pid import PID
import threading


class TemperatureControl(object):
    def __init__(self, ard, lv):
        self.ard = ard
        self.lv = lv
        
        #PID controller
        self.pid = PID()
        self.pid.sample_time = 0.1 #update every 1s
        self.pid.output_limits = (0, 1) #Amps on output
        #self.pid.tunings = (0.1, 0.1, 8)
        self.pid.auto_mode = True

        #thread the temp control process
        self.pill2kill = threading.Event()
        self.controlThread = threading.Thread(target=self.controlCurrent, args=(self.pill2kill, 'test'))

        self.settemp = 30
        self.running = False
        
    def setTemperature(self, temp):
        self.pid.setpoint = temp
        self.settemp = temp


    def controlCurrent(self, killme, arg):
        self.running = True
        while True:
            temp = self.ard.getTemperature()
            curr = self.pid(temp) 
            self.lv.setCurrent(curr)
            #print(temp, curr)
            if killme.wait(0.005):
                return

    def stopControl(self):
        self.running = False
        self.pill2kill.set()
        self.controlThread.join(2)
        self.lv.setCurrent(0)
        self.pill2kill = threading.Event()
        self.controlThread = threading.Thread(target=self.controlCurrent, args=(self.pill2kill, 'test'))



        
        
        
    
    
    
