from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import random


class LiveMonitor(object):
    
    def __init__(self):
        self.fig = plt.figure(1)                            #instance to plot on
        self.canvas = FigureCanvas(self.fig)                #canvas widget to display figure
        
        #waveform plot
        self.time_arr = None
        self.wfa_arr = None     #fist wf
        self.wfo_arr = None     #last wf
        
        #2D scan plot
        self.x = []
        self.y = []
        self.z = []
        self.sp = []
               
    def setWaveform(self, timea, wfa, wfo):
        self.time_arr = timea
        self.wfa_arr = wfa
        self.wfo_arr = wfo
    
    def setScanPoint(self, x, y, z, val):
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)
        self.sp.append(val)

    

    def updatePlots(self):
        data = [random.random() for i in range(10)]
        
        wf = self.fig.add_subplot(211)
        wf.hold(False) #discards the old graph
        wf.plot(self.time_arr, self.wfa_arr, 'k', self.time_arr, self.wfo_arr, 'r') #first wf: black, second one: red
        
        scan = self.fig.add_subplot(212)
        scan.hold(False) #discards the old graph
        scan.scatter(-1.0*np.array(self.x), -1.0*np.array(self.y), c=np.array(self.sp),edgecolors='none')

        plt.tight_layout(pad=1, w_pad=0.5, h_pad=2)
        self.canvas.draw()
        
        


        