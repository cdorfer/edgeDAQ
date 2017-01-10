from time import sleep

class MovementControl:
    def __init__(self, stage, axes):
        self.stage = stage
        self.xaxis = axes[0]
        self.yaxis = axes[1]
        self.zaxis = axes[2]
        
    def moveStepX(self, direction, step): 
        self.xaxis.move_by((direction*step), wait=True)
        
    def moveStepY(self, direction, step):
        self.yaxis.move_by((direction*step), wait=True)
        
    def moveStepZ(self, direction, step):
        self.zaxis.move_by((direction*step), wait=True)
        
    def moveAbsoluteX(self, position): 
        self.xaxis.move_to((position), wait=True)
        
    def moveAbsoluteY(self, position):
        self.yaxis.move_by((position), wait=True)
        
    def moveAbsoluteZ(self, position):
        self.zaxis.move_by((position), wait=True)    
    
    def getXPosition(self):
        return self.xaxis.position
        
    def getYPosition(self):
        return self.yaxis.position
    
    def getZPosition(self):
        return self.zaxis.position
  
        


class PositionControl:
    def __init__(self, stage, axes):
        self.stage = stage
        self.xaxis = axes[0]
        self.yaxis = axes[1]
        self.zaxis = axes[2]
        
        self.xlimlow = 0
        self.xlimhigh = 0
        self.ylimlow = 0
        self.ylimhigh = 0
        self.zlimlow = 0
        self.zlimhigh = 0
                         
    def getCurrentHome(self):  
        return (self.xaxis.home, self.yaxis.home, self.zaxis.home)
                
    def setHome(self):
        self.xlimlow =  self.xlimlow -self.xaxis.position
        self.xlimhigh = self.xlimhigh - self.xaxis.position
        self.xaxis.home = 0
        print self.xlimlow, self.xaxis.position, self.xlimhigh
        
        self.ylimlow = self.ylimlow - self.yaxis.position 
        self.ylimhigh = self.ylimhigh - self.yaxis.position
        self.yaxis.home = 0
        print self.ylimlow, self.yaxis.position, self.ylimhigh
        
        self.zlimlow = self.zlimlow - self.zaxis.position
        self.zlimhigh = self.zlimhigh - self.zaxis.position
        self.zaxis.home = 0
        print self.zlimlow, self.zaxis.position, self.zlimhigh
               
    def goHome(self):
        self.xaxis.home_search(0)
        self.yaxis.home_search(0)
        self.zaxis.home_search(0)
          
    def findHardwareLimits(self):
        print 'Turning axes on.'
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
        if (self.xmax > self.xmin and self.xstep <= 0) or (self.xmin > self.xmax and self.xstep >= 0) or (abs(self.xstep) > abs(self.xmax - self.xmin)):
            print 'Check x-limits and step direction/size.'
            return
        
        if (self.ymax > self.ymin and self.ystep <= 0) or (self.ymin > self.ymax and self.ystep >= 0) or (abs(self.ystep) > abs(self.ymax - self.ymin)):
            print 'Check y-limits and step direction/size.'
            return
        
        if (self.zmax > self.zmin and self.zstep <= 0) or (self.zmin > self.zmax and self.zstep >= 0) or (abs(self.zstep) > abs(self.zmax - self.zmin)):
            print 'Check z-limits and step direction/size.'
            return
        
        print 'Turning axes on.'
        self.xaxis.on()
        self.yaxis.on()
        self.zaxis.on()
        sleep(1)  
        
        #calculate number of required steps
        xsteps = abs((self.xmin - self.xmax)/self.xstep)
        ysteps = abs((self.ymin - self.ymax)/self.ystep)
        zsteps = abs((self.zmin - self.zmax)/self.zstep)
        
        #scan along focus axis
        for idz in xrange(int(zsteps)+1):
            znext = self.zmin+idz*self.zstep
            if self.zactive:
                self.zaxis.move_to(znext, wait=True)
            
            #along y-axis (up - down)
            for idx in xrange(int(ysteps)+1):
                ynext = self.ymin+idx*self.ystep
                if self.yactive:
                    self.yaxis.move_to(ynext, wait=True)
        
                #along x-axis (left - right)
                for idy in xrange(int(xsteps)+1):
                    xnext = self.xmin+idy*self.xstep
                    if self.xactive:
                        self.xaxis.move_to(xnext, wait=True)
                    
                    if (self.running == False):
                        return
                    
                    sleep(0.5)
                    # do oscilloscope readout here
                                          
    def startScan(self):
        self.running = True
        self.theScan()
    
    def stopScan(self):    
        self.running = False
    
  
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