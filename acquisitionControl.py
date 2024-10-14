####################################               
# Author: Christian Dorfer
# Email: cdorfer@phys.ethz.ch                                  
####################################

from time import sleep, time
import datetime
import numpy as np
import h5py


class AcquisitionControl(object):
    def __init__(self, xps, tektronix, datahandler, configuration): 
        self.xps = xps
        
        self.tek = tektronix
        self.dh = datahandler
        self.config = configuration

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
        #some sanity checks
        if(self.xactive):
            if (self.xScanMax > self.xScanMin and self.xScanStep <= 0) or (self.xScanMin > self.xScanMax and self.xScanStep >= 0) or (abs(self.xScanStep) > abs(self.xScanMax - self.xScanMin)):
                print('Check x-limits and step direction/size.')
                return

        
        if(self.yactive):
            if (self.yScanMax > self.yScanMin and self.yScanStep <= 0) or (self.yScanMin > self.yScanMax and self.yScanStep >= 0) or (abs(self.yScanStep) > abs(self.yScanMax - self.yScanMin)):
                print('Check y-limits and step direction/size.')
                return

        
        if(self.zactive):
            if (self.zScanMax > self.zScanMin and self.zScanStep <= 0) or (self.zScanMin > self.zScanMax and self.zScanStep >= 0) or (abs(self.zScanStep) > abs(self.zScanMax - self.zScanMin)):
                print('Check z-limits and step direction/size.')
                return


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
                self.xps.move_z(znext)
            
            #along y-axis (up - down)
            for idy in range(int(ysteps)+1):
                if self.yactive:
                    ynext = self.yScanMin+idy*self.yScanStep
                    self.xps.move_y(ynext)
        
                #along x-axis (left - right)
                for idx in range(int(xsteps)+1):
                    if self.xactive:
                        xnext = self.xScanMin+idx*self.xScanStep
                        self.xps.move_x(xnext)
                    
                    #check if thread was terminated
                    startt = datetime.datetime.now()
                    if stop_event.wait(0.005):
                        print('Scan finished.')
                        return
                        
                    print("x: %.2f" %self.xaxis.position, " y: %.2f" %self.yaxis.position, " z: %.2f" %self.zaxis.position)
                    #nsp = self.collectNWfs()
                    endt = datetime.datetime.now()
                    #print('Scanpoint ', nsp, '/', self.nScanPoints, ' written to file (', round(((endt-startt).total_seconds()*1000),1), ' ms )')
                    sleep(0.02)

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
        nsp = self.dh.addScanPointData(timestamp, self.xps.get_xpos(), self.xps.get_ypos(), self.xps.get_zpos(), scaledtime, scaleddata)
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
        print('value problemo: ', val)
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
    
