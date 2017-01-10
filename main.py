from newportESP import ESP
from daq import MovementControl, PositionControl, ScanControl

#def main():
    

    

if __name__ == '__main__':
    #main()
    #open serial connection to newport table
    esp = ESP('/dev/ttyUSB0')
    axes = [esp.axis(2), esp.axis(3), esp.axis(1)] #x, y, z
    
    #initialize classes
    movecontr = MovementControl(esp, axes)
    poscontr = PositionControl(esp, axes)
    scancontr = ScanControl(esp, axes)
    
    poscontr.findHardwareLimits()
    poscontr.setHome()
    axes[0].on()
    axes[1].on()
    axes[2].on()
    
    
    axes[0].move_by(20, wait=True)
    axes[1].move_by(1.5, wait=True)
    axes[2].move_by(-30, wait=True)
    poscontr.setHome()
    
    
    scancontr.setZmin(6) #zStart
    scancontr.setZmax(-6) #zStop
    scancontr.setStepZ(-0.05) #zStep
    
    scancontr.setXmin(0)
    scancontr.setXmax(10)
    scancontr.setStepX(1)
    
    scancontr.setYmin(0)
    scancontr.setYmax(2)
    scancontr.setStepY(1)
    
    print 'starting scan'
    #scancontr.startScan()
    