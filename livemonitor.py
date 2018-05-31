####################################              
# Author: Christian Dorfer
# Email: cdorfer@phys.ethz.ch                                  
####################################

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from drawnow import drawnow
import matplotlib.pyplot as plt


class LiveMonitor(object):
    
    def __init__(self):
        self.fig = plt.figure()                             #instance to plot on
        self.g1 = self.fig.add_subplot(211)                 #graph for waveform plotting
        self.g1.set_xlabel('Time [ns]')
        self.g1.set_ylabel('Amplitude [mv]')
        self.g2 = self.fig.add_subplot(212)                 #graph to plot 2d scan map
        self.g2.set_xlabel('x [mm]')
        self.g2.set_ylabel('y [mm]')
        self.canvas = FigureCanvas(self.fig)                #canvas widget to display figure
        self.canvas.draw()

        self.enabled = True

        #waveform plot
        self.time_arr = None
        self.wfa_arr = None     #fist wf
        self.wfo_arr = None     #last wf
        self.fig1 = None
        self.fig2 = None
        
        #2D scan plot parameters
        self.xmin = 0
        self.xmax = 0
        self.xstep = 0
        
        self.ymin = 0
        self.ymax = 0
        self.ystep = 0
        
        self.zmin = 0
        self.zmax = 0
        self.zstep = 0
        
        #values for 2D scan histogram
        self.x = []
        self.y = []
        self.z = []
        self.sp = []

        

    def enablePlotting(self, arg):
        if arg == True:
            self.enabled = True

        else:
            self.enabled = False
            self.g1.clear()
            self.g2.clear()
            self.canvas.draw()

    def resetPlots(self):
        self.time_arr = None
        self.wfa_arr = None     #fist wf
        self.wfo_arr = None     #last wf
        
        self.x = []
        self.y = []
        self.z = []
        self.sp = []
        
        self.g1.clear()
        self.g2.clear()

        self.canvas.draw()
    
      
    def setWaveform(self, timea, wfa, wfo):
        self.time_arr = timea*1e9
        self.wfa_arr = wfa*1e3
        self.wfo_arr = wfo*1e3
    
    def setScanPoint(self, x, y, z, val):
        self.x.append(round(x, 4))
        self.y.append(round(y,4))
        self.z.append(round(z,4))
        self.sp.append(str(((val+50.0)/500))) #fixme - value can only be between 0-1

    def setStepSize(self, ss):
        (self.xstep, self.ystep, self.zstep) = ss
        
    def setPlotLimits(self, sl):
        (self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax) = sl


    def updatePlots(self): 
        if self.enabled: #if plotting is enabled
            self.g1.clear()
            self.g1.plot(self.time_arr, self.wfa_arr, 'k', self.time_arr, self.wfo_arr, 'r') #first wf: black, second one: red

            if(len(self.x) != 0):
                self.g2.clear()
                n = len(self.sp) #to prevent racing conditions
                self.g2.scatter(self.x[0:n], self.y[0:n], c=self.sp[0:n], s=100, cmap='jet',edgecolors='none', marker='s')   
            
            try:
                self.canvas.draw()
            except:
                pass


        