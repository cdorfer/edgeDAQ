from time import sleep
  
class PositionControl(object):
    def __init__(self, stage, axes):
        self.stage = stage
        self.xaxis = axes[0]
        self.yaxis = axes[1]
        self.zaxis = axes[2]
        
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
        
  
class ScanControl(object):
    def __init__(self, stage, axes): # plus osci later
        self.stage = stage
        self.xaxis = axes[0]
        self.yaxis = axes[1]
        self.zaxis = axes[2]
        
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        self.zmin = 0
        self.zmax = 0
        
        self.xstep = 0
        self.ystep = 0
        self.zstep = 0
        
        self.xactive = True
        self.yactive = True
        self.zactive = True
        self.running = False
 
    
    def theScan(self):

        #some sanity checks
        if(self.xactive):
            if (self.xmax > self.xmin and self.xstep <= 0) or (self.xmin > self.xmax and self.xstep >= 0) or (abs(self.xstep) > abs(self.xmax - self.xmin)):
                print('Check x-limits and step direction/size.')
                return
            self.xaxis.on()
        
        if(self.yactive):
            if (self.ymax > self.ymin and self.ystep <= 0) or (self.ymin > self.ymax and self.ystep >= 0) or (abs(self.ystep) > abs(self.ymax - self.ymin)):
                print('Check y-limits and step direction/size.')
                return
            self.yaxis.on()
        
        if(self.zactive):
            if (self.zmax > self.zmin and self.zstep <= 0) or (self.zmin > self.zmax and self.zstep >= 0) or (abs(self.zstep) > abs(self.zmax - self.zmin)):
                print('Check z-limits and step direction/size.')
                return
            self.zaxis.on()
             
        sleep(1)  
        
        #calculate number of required steps
        xsteps = abs((self.xmin - self.xmax)/self.xstep)
        ysteps = abs((self.ymin - self.ymax)/self.ystep)
        zsteps = abs((self.zmin - self.zmax)/self.zstep)
        
        #scan along focus axis
        if not self.zactive:
            zsteps = 0
        if not self.yactive:
            ysteps = 0
        if not self.xactive:
            xsteps = 0
            
        
        
        for idz in range(int(zsteps)+1):
            if self.zactive:
                znext = self.zmin+idz*self.zstep
                self.zaxis.move_to(znext, wait=True)
            
            #along y-axis (up - down)
            for idx in range(int(ysteps)+1):
                if self.yactive:
                    ynext = self.ymin+idx*self.ystep
                    self.yaxis.move_to(ynext, wait=True)
        
                #along x-axis (left - right)
                for idy in range(int(xsteps)+1):
                    if self.xactive:
                        xnext = self.xmin+idy*self.xstep
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
        self.xmin = val
        
    def setXmax(self, val):
        self.xmax = val
        
    def setYmin(self, val):
        self.ymin = val
        
    def setYmax(self, val):
        self.ymax = val
        
    def setZmin(self, val):
        self.zmin = val
        
    def setZmax(self, val):
        self.zmax = val
     
    def setStepX(self, val):
        self.xstep = val
        
    def setStepY(self, val):
        self.ystep = val
        
    def setStepZ(self, val):
        self.zstep = val
    
    
    def getXmin(self):
        return self.xmin
    
    def getXmax(self):
        return self.xmax
        
    def getYmin(self):
        return self.ymin
        
    def getYmax(self):
        return self.ymax
        
    def getZmin(self):
        return self.zmin
        
    def getZmax(self):
        return self.zmax    
        
    def getStepX(self):
        return self.xstep
        
    def getStepY(self):
        return self.ystep
        
    def getStepZ(self):
        return self.zstep