from time import sleep
import datetime
import numpy as np
import h5py
import tektronix

class DataHandling(object):
    """
    Usage:
    dh = DataHandling()
    dh.createFile()
    
    t = np.random.random(size=1000)
    dh.setTimScale(t)
    
    a = np.random.random(size=(400,1000))
    dh.addScanPointData(a)
    dh.addScanPointData(a)
    dh.addScanPointData(a)
    
    dh.closeFile()
    """
     
    def __init__(self):
        self.hdf = None
        self.tctdata = None
        self.spcount = 1

        #parameters that are set through the GUI (at startup read from configuration file)
        self.diamond_name = "S119"
        self.side = 1
        self.bias_voltage = "-400"
        self.laser_pulse_energy = "5" #pJ
        
        #self.createFile()

    def createFile(self):
        #read and increase run number
        self.runnumber = self.increaseRunNumber()
         
        #create new h5py file
        fname = 'data/run' + str(self.runnumber) + ".hdf5"
        self.hdf = h5py.File(fname, "w", libver='latest')
        self.hdf.attrs['timestamp'] = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

        self.tctdata = self.hdf.create_group("tctdata")
        self.tctdata.attrs['diamond_name'] = self.diamond_name
        self.tctdata.attrs['side'] = self.side
        self.tctdata.attrs['bias_voltage'] = self.bias_voltage
        self.tctdata.attrs['laser_pulse_energy'] = self.laser_pulse_energy
    
        
    def setTimScale(self, time_array):    
        self.tctdata.attrs['time_array'] = time_array
        
    
    def addScanPointData(self, arr):
        sp = str(self.spcount)
        print("Writing data for scanpoint ", sp)
        self.tctdata.create_dataset(sp, data=arr)
        self.spcount += 1
        
    
    def increaseRunNumber(self):
        with open('data/runnumber.dat', "r+") as f:
            runnumber = int(f.readline())
            f.seek(0)
            f.write(str(runnumber+1))
        return runnumber
        
        
    def closeFile(self):
        self.hdf.flush()
        self.hdf.close()




class PositionControl(object):
    def __init__(self, stage, axes, config):
        self.stage = stage
        self.xaxis = axes[0]
        self.yaxis = axes[1]
        self.zaxis = axes[2]
        
        self.xStepSize = config.getfloat('PositionControl', 'xStepSize')
        self.yStepSize = config.getfloat('PositionControl', 'yStepSize')
        self.zStepSize = config.getfloat('PositionControl', 'zStepSize')
        
        #hardware limits:
        self.xlimlow = -50 # all in mm
        self.xlimhigh = 50
        self.ylimlow = -2.5
        self.ylimhigh = 2.5
        self.zlimlow = -75
        self.zlimhigh = 75
            
    def moveAbsoluteX(self, position): 
        self.xaxis.on()
        self.xaxis.move_to((position), wait=True)
        
    def moveAbsoluteY(self, position):
        self.yaxis.on()
        self.yaxis.move_to((position), wait=True)
        
    def moveAbsoluteZ(self, position):
        self.zaxis.on()
        self.zaxis.move_to((position), wait=True)   
        
    def moveStepX(self, step): 
        self.xaxis.on()
        self.xaxis.move_by((step), wait=True)
        
    def moveStepY(self, step):
        self.yaxis.move_by((step), wait=True)
        
    def moveStepZ(self, step):
        self.zaxis.move_by((step), wait=True)    
    
    def getXPosition(self):
        return self.xaxis.position
        
    def getYPosition(self):
        return self.yaxis.position
    
    def getZPosition(self):
        return self.zaxis.position
      
    def getXMax(self):
        return self.xlimhigh
        
    def getYMax(self):
        return self.ylimhigh
    
    def getZMax(self):
        return self.zlimhigh
    
    def getXMin(self):
        return self.xlimlow
        
    def getYMin(self):
        return self.ylimlow
    
    def getZMin(self):
        return self.zlimlow
                        
    def getCurrentHome(self):  
        return (self.xaxis.home, self.yaxis.home, self.zaxis.home)
                
    def setHome(self):
        self.xlimlow =  self.xlimlow -self.xaxis.position
        self.xlimhigh = self.xlimhigh - self.xaxis.position
        self.xaxis.home = 0
        #print(self.xlimlow, self.xaxis.position, self.xlimhigh)
        
        self.ylimlow = self.ylimlow - self.yaxis.position 
        self.ylimhigh = self.ylimhigh - self.yaxis.position
        self.yaxis.home = 0
        #print(self.ylimlow, self.yaxis.position, self.ylimhigh)
        
        self.zlimlow = self.zlimlow - self.zaxis.position
        self.zlimhigh = self.zlimhigh - self.zaxis.position
        self.zaxis.home = 0
        #print(self.zlimlow, self.zaxis.position, self.zlimhigh)
               
    def goHome(self):
        self.xaxis.home_search(0)
        self.yaxis.home_search(0)
        self.zaxis.home_search(0)
          
    def findHardwareLimits(self):
        self.xaxis.on()
        self.yaxis.on()
        self.zaxis.on()
        sleep(1) 

        self.xaxis.move_to_hardware_limit(-1, wait=True)
        self.xlimlow = self.xaxis.position
        self.xaxis.move_to_hardware_limit(1, wait=True)
        self.xlimhigh = self.xaxis.position
        self.xaxis.move_to((self.xlimlow+self.xlimhigh)/2, wait=True)
               
        self.zaxis.move_to_hardware_limit(-1, wait=True)
        self.zlimlow = self.zaxis.position
        self.zaxis.move_to_hardware_limit(1, wait=True)
        self.zlimhigh = self.zaxis.position
        self.zaxis.move_to((self.zlimlow+self.zlimhigh)/2, wait=True)
              
        self.yaxis.move_to_hardware_limit(-1, wait=True)
        self.ylimlow = self.yaxis.position
        self.yaxis.move_to_hardware_limit(1, wait=True)
        self.ylimhigh = self.yaxis.position
        self.yaxis.move_to((self.ylimlow+self.ylimhigh)/2, wait=True)
        


class AcquisitionControl(object):
    def __init__(self, stage, axes, tektronix, datahandler, configuration): # plus osci later
        self.stage = stage
        self.xaxis = axes[0]
        self.yaxis = axes[1]
        self.zaxis = axes[2]
        
        self.tek = tektronix
        self.dh = datahandler
        self.config = configuration
        
        self.xScanMin = self.config.getfloat('AcquisitionControl', 'xMin')
        self.xScanMax = self.config.getfloat('AcquisitionControl', 'xMax')
        self.xScanStep =self.config.getfloat('AcquisitionControl', 'xStep') 
        
        self.yScanMin = self.config.getfloat('AcquisitionControl', 'yMin')
        self.yScanMax = self.config.getfloat('AcquisitionControl', 'yMax')
        self.yScanStep =self.config.getfloat('AcquisitionControl', 'yStep')
        
        self.zScanMin = self.config.getfloat('AcquisitionControl', 'zMin')
        self.zScanMax = self.config.getfloat('AcquisitionControl', 'zMax')
        self.zScanStep =self.config.getfloat('AcquisitionControl', 'zStep')
        
        self.xactive = True
        self.yactive = True
        self.zactive = True
        self.running = False
 
    
    def theScan(self):
        
        #configure the oscilloscope for data taking
        self.tek.configure()

        #some sanity checks
        if(self.xactive):
            if (self.xScanMax > self.xScanMin and self.xScanStep <= 0) or (self.xScanMin > self.xScanMax and self.xScanStep >= 0) or (abs(self.xScanStep) > abs(self.xScanMax - self.xScanMin)):
                print('Check x-limits and step direction/size.')
                return
            self.xaxis.on()
        
        if(self.yactive):
            if (self.yScanMax > self.yScanMin and self.yScanStep <= 0) or (self.yScanMin > self.yScanMax and self.yScanStep >= 0) or (abs(self.yScanStep) > abs(self.yScanMax - self.yScanMin)):
                print('Check y-limits and step direction/size.')
                return
            self.yaxis.on()
        
        if(self.zactive):
            if (self.zScanMax > self.zScanMin and self.zScanStep <= 0) or (self.zScanMin > self.zScanMax and self.zScanStep >= 0) or (abs(self.zScanStep) > abs(self.zScanMax - self.zScanMin)):
                print('Check z-limits and step direction/size.')
                return
            self.zaxis.on()
             
        sleep(1)  
        
        #calculate number of required steps
        xsteps = abs((self.xScanMin - self.xScanMax)/self.xScanStep)
        ysteps = abs((self.yScanMin - self.yScanMax)/self.yScanStep)
        zsteps = abs((self.zScanMin - self.zScanMax)/self.zScanStep)
        
        #scan along focus axis
        if not self.zactive:
            zsteps = 0
        if not self.yactive:
            ysteps = 0
        if not self.xactive:
            xsteps = 0
            
        
        
        for idz in range(int(zsteps)+1):
            if self.zactive:
                znext = self.zScanMin+idz*self.zScanStep
                self.zaxis.move_to(znext, wait=True)
            
            #along y-axis (up - down)
            for idx in range(int(ysteps)+1):
                if self.yactive:
                    ynext = self.yScanMin+idx*self.yScanStep
                    self.yaxis.move_to(ynext, wait=True)
        
                #along x-axis (left - right)
                for idy in range(int(xsteps)+1):
                    if self.xactive:
                        xnext = self.xScanMin+idy*self.xScanStep
                        self.xaxis.move_to(xnext, wait=True)
                    
                    if (self.running == False):
                        return
                    print("x: %.2f" %self.xaxis.position, " y: %.2f" %self.yaxis.position, " z: %.2f" %self.zaxis.position)
                    sleep(1)
                    # do oscilloscope readout here
   
                                          
    def startScan(self):
        self.running = True
        print('Starting a scan.')
        self.theScan()
    
    def stopScan(self):    
        self.running = False
    
  
    def setXactive(self, val):
        self.xactive = val

    def setYactive(self, val):
        self.yactive = val

    def setZactive(self, val):
        self.zactive = val
  
    #setter and getter methods
    def setXmin(self, val):
        self.xScanMin = val
        
    def setXmax(self, val):
        self.xScanMax = val
        
    def setYmin(self, val):
        self.yScanMin = val
        
    def setYmax(self, val):
        self.yScanMax = val
        
    def setZmin(self, val):
        self.zScanMin = val
        
    def setZmax(self, val):
        self.zScanMax = val
     
    def setStepX(self, val):
        self.xScanStep = val
        
    def setStepY(self, val):
        self.yScanStep = val
        
    def setStepZ(self, val):
        self.zScanStep = val
    
    
    def getRunNumber(self):
        return self.dh.runnumber
    
    
    def getXmin(self):
        return self.xScanMin
    
    def getXmax(self):
        return self.xScanMax
        
    def getYmin(self):
        return self.yScanMin
        
    def getYmax(self):
        return self.yScanMax
        
    def getZmin(self):
        return self.zScanMin
        
    def getZmax(self):
        return self.zScanMax    
        
    def getStepX(self):
        return self.xScanStep
        
    def getStepY(self):
        return self.yScanStep
        
    def getStepZ(self):
        return self.zScanStep