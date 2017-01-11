import sys

#Hardware imports
from newportESP import ESP

#DAQ imports
from daq import PositionControl, ScanControl

#GUI imports
from gui import Window
from PyQt5.QtWidgets import QApplication

    

    

if __name__ == '__main__':
    
    # Create an instance of the application window and run it
    app = QApplication(sys.argv)
    
    #open serial connection to newport table
    esp = ESP('/dev/ttyUSB0')
    axes = [esp.axis(2), esp.axis(3), esp.axis(1)] #x, y, z
    
    #initialize classes
    posContr = PositionControl(esp, axes)
    
    scanContr = ScanControl(esp, axes)
       
    window = Window(posContr, scanContr)
    sys.exit(app.exec_())
    



    
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
    