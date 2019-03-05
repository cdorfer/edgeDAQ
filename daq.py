####################################               
# Author: Christian Dorfer
# Email: cdorfer@phys.ethz.ch                                  
####################################

from time import sleep, time
import datetime
from _thread import start_new_thread
import numpy as np
import h5py
from hvinterface import HVInterface


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
     
    def __init__(self, conf, livemon):
        self.hdf = None
        self.tctdata = None
        self.spcount = 1
        self.runnumber = self.readRunNumber()+1
        self.config = conf
        self.livemon = livemon

        #parameters that are set through the GUI (at startup read from configuration file)
        self.diamond_name = self.config['AcquisitionControl']['diamond_name']
        self.side = int(self.config['AcquisitionControl']['side'])
        self.bias_voltage = float(self.config['AcquisitionControl']['bias_voltage'])
        self.amplifier = self.config['AcquisitionControl']['amplifier']
        self.scan_type = self.config['AcquisitionControl']['scan_type']
        self.laser_pulse_energy = float(self.config['AcquisitionControl']['laser_pulse_energy'])
        self.pcb = self.config['AcquisitionControl']['pcb']
        self.nwf = int(self.config['AcquisitionControl']['number_of_waveforms'])
        
        #self.createFile()

    def createFile(self, comment):
        
        #reset old one
        self.hdf= None
        self.tctdata = None
        self.spcount = 0
        
        #read and increase run number
        self.runnumber = self.increaseRunNumber()
        print('Run number: ', self.runnumber)
         
        #create new h5py file
        fname = 'data/run' + str(self.runnumber) + ".hdf5"
        self.hdf = h5py.File(fname, "w", libver='latest')
        self.hdf.attrs['timestamp'] = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        self.tctdata = self.hdf.create_group("tctdata")
        self.tctdata.attrs['diamond_name'] = self.diamond_name
        self.tctdata.attrs['bias_voltage'] = self.bias_voltage
        self.tctdata.attrs['number_of_waveforms'] = self.nwf
        self.tctdata.attrs['laser_pulse_energy'] = self.laser_pulse_energy
        self.tctdata.attrs['side'] = self.side
        self.tctdata.attrs['amplifier'] = self.amplifier
        self.tctdata.attrs['scan_type'] = self.scan_type
        self.tctdata.attrs['pcb'] = self.pcb
        self.tctdata.attrs['comments'] = comment
        print('File ', fname, ' created.')
        
    
    def addScanPointData(self, timestamp, x,y,z, time_axis, wfarr):
        sp = str(self.spcount)
        self.tctdata.create_dataset(sp, data=wfarr, compression="gzip")
        self.tctdata[sp].attrs['timestamp'] = timestamp
        self.tctdata[sp].attrs['x'] = x
        self.tctdata[sp].attrs['y'] = y
        self.tctdata[sp].attrs['z'] = z
        self.tctdata[sp].attrs['time_axis'] = time_axis
        self.spcount += 1
        #print('Scanpoint ', sp, ' written to file.')
            
        #send data to online monitor
        self.livemon.setWaveform(time_axis, wfarr[0:len(time_axis)], wfarr[len(wfarr)-len(time_axis):len(wfarr)]) #wf plot
        #self.livemon.setScanPoint(x, y, z, np.sum(wfarr[0:len(time_axis)]))
        self.livemon.setScanPoint(x, y, z, np.sum(wfarr[0:len(time_axis)]))
        
        #start_new_thread(self.livemon.updatePlots, ())
        return sp
        
    def setTemperature(self, val):

        self.tctdata.attrs['temperature'] = val
        print('Setting temperature: {}'.format(val))

    def increaseRunNumber(self):
        with open('data/runnumber.dat', "r+") as f:
            runnumber = int(f.readline())
            f.seek(0)
            f.write(str(runnumber+1))
            return (runnumber+1)
            
    def readRunNumber(self):
        with open('data/runnumber.dat', "r") as f:
            return int(f.readline())
        
    def closeFile(self):
        self.hdf.flush()
        self.hdf.close()
        self.livemon.resetPlots()
        print('File for run ', str(self.runnumber), ' closed.')
    


    #setter methods to write GUI values back to the configuration file
    def setDiamondName(self, val):
        self.diamond_name = val
        self.config['AcquisitionControl']['diamond_name'] = val
        self.config.write()

    def setSide(self, val):
        self.side = val
        self.config['AcquisitionControl']['side'] = int(val)
        self.config.write()

    def setBiasVoltage(self, val):
        self.bias_voltage = val
        self.config['AcquisitionControl']['bias_voltage'] = val
        self.config.write()
        
    def setLaserPulseEnergy(self, val):
        self.laser_pulse_energy = val
        self.config['AcquisitionControl']['laser_pulse_energy'] = val
        self.config.write()
    
    ''' function replaced by set scan type
    def setAmplifier(self, val):
        self.amplifier = val
        self.config['AcquisitionControl']['amplifier'] = val
        self.config.write()
    '''

    def setScanType(self, val):
        self.scan_type = val
        self.config['AcquisitionControl']['scan_type'] = val
        self.config.write()


    def setPCB(self, val):
        self.pcb = val
        self.config['AcquisitionControl']['pcb'] = val
        self.config.write()
        
    def setNWf(self, val):
        self.nwf = val
        self.config['AcquisitionControl']['number_of_waveforms'] = int(val)
        self.config.write()






class PositionControl(object):
    def __init__(self, stage, axes, config):
        self.config = config
        self.stage = stage
        self.xaxis = axes[0]
        self.yaxis = axes[1]
        self.zaxis = axes[2]
        
        self.xStepSize = float(config['PositionControl']['xStepSize'])
        self.yStepSize = float(config['PositionControl']['yStepSize'])
        self.zStepSize = float(config['PositionControl']['zStepSize'])
                                                       
        #hardware limits:
        self.xlimlow = float(config['PositionControl']['xLimLow'])
        self.xlimhigh = float(config['PositionControl']['xLimHigh'])

        self.ylimlow = float(config['PositionControl']['yLimLow'])
        self.ylimhigh = float(config['PositionControl']['yLimHigh'])

        self.zlimlow = float(config['PositionControl']['zLimLow'])
        self.zlimhigh = float(config['PositionControl']['zLimHigh'])
            

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
     
    #getter methods do not return class variables but read back values from Newport table
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
                                        
        #save the limits in the config
        self.config['PositionControl']['xLimLow'] = self.xlimlow
        self.config['PositionControl']['xLimHigh'] = self.xlimhigh
        self.config['PositionControl']['yLimLow'] = self.ylimlow
        self.config['PositionControl']['yLimHigh'] = self.ylimhigh
        self.config['PositionControl']['zLimLow'] = self.zlimlow
        self.config['PositionControl']['zLimHigh'] = self.zlimhigh
        self.config.write()
        


class AcquisitionControl(object):
    def __init__(self, stage, axes, tektronix, datahandler, configuration, arduino, uvlight): # plus osci later
        self.stage = stage
        self.xaxis = axes[0]
        self.yaxis = axes[1]
        self.zaxis = axes[2]
        
        self.tek = tektronix
        self.dh = datahandler
        self.config = configuration
        self.ard = arduino
        self.hv = HVInterface()
        self.uv = uvlight

        self.xScanMin = float(self.config['AcquisitionControl']['xMin'])
        self.xScanMax = float(self.config['AcquisitionControl']['xMax'])
        self.xScanStep = float(self.config['AcquisitionControl']['xStep']) 
                           
        self.yScanMin = float(self.config['AcquisitionControl']['yMin'])
        self.yScanMax = float(self.config['AcquisitionControl']['yMax'])
        self.yScanStep = float(self.config['AcquisitionControl']['yStep'])
                                       
        self.zScanMin = float(self.config['AcquisitionControl']['zMin'])
        self.zScanMax = float(self.config['AcquisitionControl']['zMax'])
        self.zScanStep = float(self.config['AcquisitionControl']['zStep'])
        
        self.xactive = False
        self.yactive = False
        self.zactive = False
        self.running = False

        self.nScanPoints = 0
 
    
    def startScan(self, stop_event, arg): 
        self.dh.setTemperature(self.ard.getStoredTemperature())


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
            for idy in range(int(ysteps)+1):
                if self.yactive:
                    ynext = self.yScanMin+idy*self.yScanStep
                    self.yaxis.move_to(ynext, wait=True)

                #along x-axis (left - right)
                for idx in range(int(xsteps)+1):
                    if self.xactive:
                        xnext = self.xScanMin+idx*self.xScanStep
                        self.xaxis.move_to(xnext, wait=True)
                    
                    #check if thread was terminated
                    startt = datetime.datetime.now()
                    if stop_event.wait(0.005):
                        print('Scan finished.')
                        return

                    self.ard.open(False)
                    self.hv.setVoltage(0)
                    sleep(10)
                    self.uv.switchLED(1)
                    sleep(10)
                    self.uv.switchLED(0)
                    sleep(1)
                    self.hv.setVoltage(500)
                    sleep(10)
                    self.ard.open(True) 

                    sleep(0.1)
                    for n in range(5):
                        nsp = self.collectNWfs()
                        sleep(4)


                    #print("x: %.2f" %self.xaxis.position, " y: %.2f" %self.yaxis.position, " z: %.2f" %self.zaxis.position)

                    #nsp = self.collectNWfs()
                    endt = datetime.datetime.now()
                    print('Scanpoint ', nsp, '/', self.nScanPoints, ' written to file (', round(((endt-startt).total_seconds()*1000),1), ' ms )')
                    
        print('Scan finished.')
        return 1

    
    def openTek(self):
        self.tek.open()
        
    def closeTek(self):
        self.tek.reset()
        self.tek.close()
    
    def configureTek(self):
        self.tek.configure()
  
  
    def collectNWfs(self):
        timestamp = time()
        #print('1: targety: ', round(xnext,4), 'actualy: ', self.yaxis.position, 'difference=', round(xnext-self.yaxis.position,4))
        (scaleddata, scaledtime) = self.tek.acquireWaveforms()
        nsp = self.dh.addScanPointData(timestamp, self.xaxis.position, self.yaxis.position, self.zaxis.position, scaledtime, scaleddata)
        #print('2: targety: ', round(xnext,4), 'actualy: ', self.yaxis.position, 'difference=', round(xnext-self.yaxis.position,4))

        return nsp

    def setXactive(self, val):
        self.xactive = val
        self.estimateScanSteps()

    def setYactive(self, val):
        self.yactive = val
        self.estimateScanSteps()

    def setZactive(self, val):
        self.zactive = val
        self.estimateScanSteps()
  
    #setter methods
    def setXmin(self, val):
        self.xScanMin = val
        self.config['AcquisitionControl']['xMin'] = val
        self.config.write()
        self.estimateScanSteps()
        
    def setXmax(self, val):
        self.xScanMax = val
        self.config['AcquisitionControl']['xMax'] = val
        self.config.write()
        self.estimateScanSteps()
        

    def setYmin(self, val):
        self.yScanMin = val
        self.config['AcquisitionControl']['yMin'] = val
        self.config.write()
        self.estimateScanSteps()
        
    def setYmax(self, val):
        self.yScanMax = val
        self.config['AcquisitionControl']['yMax'] = val
        self.config.write()
        self.estimateScanSteps()
        

    def setZmin(self, val):
        self.zScanMin = val
        self.config['AcquisitionControl']['zMin'] = val
        self.config.write()
        self.estimateScanSteps()
        
    def setZmax(self, val):
        self.zScanMax = val
        self.config['AcquisitionControl']['zMax'] = val
        self.config.write()
        self.estimateScanSteps()
       

    def setStepX(self, val):
        self.xScanStep = val
        self.config['AcquisitionControl']['xStep'] = val
        self.config.write()
        self.estimateScanSteps()
        
    def setStepY(self, val):
        self.yScanStep = val
        self.config['AcquisitionControl']['yStep'] = val
        self.config.write()
        self.estimateScanSteps()
        
    def setStepZ(self, val):
        self.zScanStep = val
        self.config['AcquisitionControl']['zStep'] = val
        self.config.write()
        self.estimateScanSteps()


    def estimateScanSteps(self):
        #calculate a time extimate for the scan
        zpts = 1
        if self.zactive and self.zScanStep != 0:
            if self.zScanMax >= self.zScanMin:
                zpts = abs(self.zScanMax-self.zScanMin)/abs(self.zScanStep) + 1
            else:
                zpts = abs(self.zScanMin-self.zScanMax)/abs(self.zScanStep) + 1


        ypts = 1
        if self.yactive and self.yScanStep != 0:
            if self.yScanMax >= self.yScanMin:
                ypts = abs(self.yScanMax-self.yScanMin)/abs(self.yScanStep) + 1
            else:
                ypts = abs(self.yScanMin-self.yScanMax)/abs(self.yScanStep) + 1


        xpts = 1
        if self.xactive and self.xScanStep != 0:
            if self.xScanMax >= self.xScanMin:
                xpts = abs(self.xScanMax-self.xScanMin)/abs(self.xScanStep) + 1
            else:
                xpts = abs(self.xScanMin-self.xScanMax)/abs(self.xScanStep) + 1


        self.nScanPoints = int(zpts*ypts*xpts)
        print("Scan steps: ", self.nScanPoints)
    
