####################################              
# Author: Christian Dorfer
# Email: cdorfer@phys.ethz.ch                                  
####################################

#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#import matplotlib.pyplot as plt

import pyqtgraph as pg
pg.setConfigOption('background', 'w')
import numpy as np
from scipy.interpolate import griddata
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt



class LiveMonitor(object):
    def __init__(self):
        self.wf = pg.PlotWidget(title="Waveforms")
        self.wf.setLabel("bottom", "Time [ns]")
        self.wf.setLabel("left", "Amplitude [mV]")

        #2D scatter plot implementation with matplotlib
        self.fig = plt.figure()
        self.pl = self.fig.add_subplot(111) 
        self.pl.set_xlabel('x [mm]')
        self.pl.set_ylabel('y [mm]')
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()


        #waveform plot
        self.time_arr = None
        self.wfa_arr = None     #first wf
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

        self.grid_x = None
        self.grid_y = None
        self.idx = 0
        self.enabled = True
        
        #values for 2D scan histogram
        self.x = []
        self.y = []
        self.z = []
        self.sp = []


    def enablePlotting(self, arg):
        if arg:
            self.enabled = True
            self.updatePlots()
        else:
            self.enabled = False

    def setStepSize(self, ss):
        (self.xstep, self.ystep, self.zstep) = ss

    def setPlotLimits(self, sl):
        (self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax) = sl


    def setWaveform(self, timea, wfa, wfo):
        self.time_arr = timea*1e9
        self.wfa_arr = wfa*1e3
        self.wfo_arr = wfo*1e3
    
    def setScanPoint(self, x, y, z, val):
        self.x.append(round(x, 4))
        self.y.append(round(y,4))
        self.z.append(round(z,4))
        self.sp.append(val)
        self.idx = len(self.sp)


    def updatePlots(self):   
        if self.enabled:
            self.wf.clear()
            self.pl.clear()
            if self.time_arr is not None:
                if len(self.time_arr) > 0:
                    #waveforms view
                    self.wf.plot(self.time_arr, self.wfa_arr, pen='r')
                    self.wf.plot(self.time_arr, self.wfo_arr, pen='k')

                    #scatter plot view
                    if len(self.sp) > 2:
                        n = self.idx - 1
                        self.pl.scatter(self.x[:n], self.y[:n], c=self.sp[:n], s=100, cmap='jet',edgecolors='none', marker='s') 
                        self.canvas.draw()
                        #sp = (self.sp[:n] - np.min(self.sp[:n]))/np.ptp(self.sp[:n]) #normalize scan points
                        #dat = griddata((self.x[:n], self.y[:n]), sp,(self.grid_x, self.grid_y), method='nearest')
                        #self.imv.setImage(dat, scale=[self.xstep, self.ystep], axes={'x':1,'y':0})
                        

    def resetPlots(self):
        self.pl.clear()
        self.wf.clear()
        self.x = []
        self.y = []
        self.z = []
        self.sp = []


