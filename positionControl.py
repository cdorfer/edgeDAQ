class PositionControl(object):
    def __init__(self, controller, config):
        self.xps = controller
        self.conf = config
        
        self.xHome = float(config['PositionControl']['xHome'])
        self.yHome = float(config['PositionControl']['yHome'])
        self.zHome = float(config['PositionControl']['zHome'])

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
        self.xps.move_x(position)
        
    def moveAbsoluteY(self, position):
        self.xps.move_y(position)
        
    def moveAbsoluteZ(self, position):
        self.xps.move_z(position)
        
    def moveStepX(self, step):
        curr = self.getXPosition()
        self.xps.move_x(curr + step)
        
    def moveStepY(self, step):
        curr = self.getYPosition()
        self.xps.move_y(curr + step)
        
    def moveStepZ(self, step):
        curr = self.getZPosition()
        self.xps.move_z(curr + step)

    #getter methods do not return class variables but read back values from Newport table
    def getXPosition(self):
        return self.xps.get_xpos()
        
    def getYPosition(self):
        return self.xps.get_ypos()
    
    def getZPosition(self):
        return self.xps.get_zpos()
      
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
        self.conf['PositionControl']['xHome'] = self.xps.get_xpos()
        self.conf['PositionControl']['yHome'] = self.xps.get_ypos()
        self.conf['PositionControl']['zHome'] = self.xps.get_zpos()
        self.conf.write()
               

    def goHome(self):
        self.xps.move_x(self.conf['PositionControl']['xHome'])
        self.xps.move_y(self.conf['PositionControl']['yHome'])
        self.xps.move_z(self.conf['PositionControl']['zHome'])
          
