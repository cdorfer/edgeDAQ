from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np


class LiveMonitor(object):
    
    def __init__(self):
        self.fig = plt.figure()                             #instance to plot on
        self.canvas = FigureCanvas(self.fig)                #canvas widget to display figure
        
        #waveform plot
        self.time_arr = None
        self.wfa_arr = None     #fist wf
        self.wfo_arr = None     #last wf
        
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
        
    def resetPlots(self):
        self.time_arr = None
        self.wfa_arr = None     #fist wf
        self.wfo_arr = None     #last wf
        
        self.x = []
        self.y = []
        self.z = []
        self.sp = []
        
        self.fig.clf()
        self.canvas.draw()
    
      
    def setWaveform(self, timea, wfa, wfo):
        self.time_arr = timea
        self.wfa_arr = wfa
        self.wfo_arr = wfo
    
    def setScanPoint(self, x, y, z, val):
        self.x.append(round(x, 4))
        self.y.append(round(y,4))
        self.z.append(round(z,4))
        self.sp.append(val)

    def setStepSize(self, ss):
        (self.xstep, self.ystep, self.zstep) = ss
        
    def setPlotLimits(self, sl):
        (self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax) = sl


    def updatePlots(self): 
        
        self.fig.add_subplot(211)
        plt.hold(False) #discards the old graph
        plt.plot(self.time_arr, self.wfa_arr, 'k', self.time_arr, self.wfo_arr, 'r') #first wf: black, second one: red
         
    
        self.fig.add_subplot(212)
        plt.hold(False) #discards the old graph
        if(len(self.x) != 0):
            plt.scatter(self.x, self.y, c=self.sp, s=100, cmap='jet',edgecolors='none', marker='s')
        plt.tight_layout(pad=1, w_pad=0.5, h_pad=2)
        self.canvas.draw()
         


        