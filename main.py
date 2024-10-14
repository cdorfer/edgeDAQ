####################################               
# Author: Christian Dorfer
# Email: dorfer@phys.ethz.ch                                  
####################################

import sys
import argparse
from configobj import ConfigObj

#Hardware imports
from tektronixMSO64B import TektronixMSO64B
from newportXPS import XPS
from lowvoltage import LowVoltage
from tempcontrol import TemperatureControl
from uvlight import UVLight
from arduino import Arduino

#DAQ imports
from positionControl import PositionControl
from acquisitionControl import AcquisitionControl
from dataHandling import DataHandling
from livemonitor import LiveMonitor

#GUI imports
from gui import Window
from PyQt5.QtWidgets import QApplication
import numpy as np

'''
pass 'temp' as first argument to get the temperature control option
'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-tc", "--tempCtrl", action="store_true", help="Turn temperature control on/off.") 
    parser.add_argument("-uv", "--uvLight", action="store_true", help="Turn UV LEDs on/off.") 

    args = parser.parse_args()
    app = QApplication(sys.argv)
    
    #get a configuration object   
    config = ConfigObj('config.ini')
    
    #initialize the LiveMonitor class
    livemon = LiveMonitor()
    
    #create data handler
    dh = DataHandling(config, livemon)
    
    #open connection to oscilloscope and pass on the configuration file
    tek = TektronixMSO64B(config)
    tek.configure()
    
    #open ethernet connection to newport table
    xps = XPS(config)
    #axes = [esp.axis(2), esp.axis(3), esp.axis(1)] #x, y, z

    arduinoaddr = config['Arduino']['address']
    arduino = Arduino(arduinoaddr)

    
    #initialize position and scan control
    posContr = PositionControl(xps, config)
    #acqContr = AcquisitionControl(esp, axes, tek, dh, config, arduino)
    acqContr = AcquisitionControl(xps, tek, dh, config)
    
    tempctrl = None
    uvlight = None
    # if args.tempCtrl or args.uvLight:
    #     lvaddr = config['LV']['address']
    #     lvcontrol = LowVoltage(lvaddr)
        
    #     if args.tempCtrl:
    #         tempctrl = TemperatureControl(arduino, lvcontrol)
    #     if args.uvLight:
    #         uvlight = UVLight(lvcontrol)



    #create an instance of the application window and run it
    window = Window(posContr, acqContr, dh, livemon, arduino, tempctrl, uvlight)
    sys.exit(app.exec_())
    
    
    
    
    
    
 