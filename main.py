####################################               
# Author: Christian Dorfer
# Email: dorfer@phys.ethz.ch                                  
####################################

import sys
import argparse
from configobj import ConfigObj

#Hardware imports
from tektronix import TektronixMSO5204B
from newportESP import ESP
from lowvoltage import LowVoltage
from tempcontrol import TemperatureControl
from arduino import Arduino

#DAQ imports
from daq import PositionControl, AcquisitionControl, DataHandling
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
    args = parser.parse_args()
    app = QApplication(sys.argv)
    
    #get a configuration object   
    config = ConfigObj('config.ini')
    
    #initialize the LiveMonitor class
    livemon = LiveMonitor()
    
    #create data handler
    dh = DataHandling(config, livemon)
    
    #open connection to oscilloscope and pass on the configuration file
    tek = TektronixMSO5204B(config)
    #tek.configure()
    
    #open serial connection to newport table
    espaddr = config['Newport']['address']
    esp = ESP(espaddr)
    axes = [esp.axis(2), esp.axis(3), esp.axis(1)] #x, y, z

    arduinoaddr = config['Arduino']['address']
    arduino = Arduino(arduinoaddr)
    
    #initialize position and scan control
    posContr = PositionControl(esp, axes, config)
    acqContr = AcquisitionControl(esp, axes, tek, dh, config, arduino)
    
    tempctrl = None
    if args.tempCtrl:
        lvaddr = config['LV']['address']
        lvcontrol = LowVoltage(lvaddr)
        tempctrl = TemperatureControl(arduino, lvcontrol)


    #create an instance of the application window and run it
    window = Window(posContr, acqContr, dh, livemon, arduino, tempctrl)
    sys.exit(app.exec_())
    
    
    
    
    
    
    #posContr.findHardwareLimits()

    '''
    tek = TektronixMSO5204B('TCPIP0::192.168.1.111::inst0::INSTR')
    tek.configure()
    
    (wfdata, timedata) = tek.acquireWaveforms()
 
    #plot the figure with correct scaling
    plt.plot(timedata,wfdata[0:2000])
    plt.plot(timedata,wfdata[2000:4000])
    plt.plot(timedata,wfdata[98000:100000])
    plt.ylabel('Voltage (V)')
    plt.xlabel('Time (sec)')
    plt.show()
    print('Plot generated.')
    '''

    '''
    dh = DataHandling()
    dh.createFile()
    
    t = np.random.random(size=1000)
    dh.setTimScale(t)
    
    a = np.random.random(size=(400,1000))
    dh.addScanPointData(a)
    dh.addScanPointData(a)
    dh.addScanPointData(a)
    
    dh.closeFile()
    '''



    
    #poscontr.findHardwareLimits()
    #poscontr.setHome()
    #axes[0].on()
    #axes[1].on()
    #axes[2].on()
    #axes[0].move_by(20, wait=True)
    #axes[1].move_by(1.5, wait=True)
    #axes[2].move_by(-30, wait=True)
    #poscontr.setHome()
    
    
    #scancontr.setZmin(5) #zStart
    #scancontr.setZmax(-5) #zStop
    #scancontr.setStepZ(-0.1) #zStep
    #
    #scancontr.setXmin(0)
    #scancontr.setXmax(5)
    #scancontr.setStepX(0.1)
    #
    #scancontr.setYmin(0)
    #scancontr.setYmax(1)
    #scancontr.setStepY(0.1)
    #
    #print 'starting scan'
    #scancontr.setXactive(0)
    #scancontr.startScan()
    