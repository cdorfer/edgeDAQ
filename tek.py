####################################               
# Author: Christian Dorfer
# Email: cdorfer@phys.ethz.ch                                  
####################################

import sys
from configobj import ConfigObj
from time import sleep

#Hardware imports
from tektronix import TektronixMSO5204B
import matplotlib.pyplot as plt

    
if __name__ == '__main__':
    #get a configuration object   
    config = ConfigObj('config.ini')
    
   
    
    #open connection to oscilloscope and pass on the configuration file
    tek = TektronixMSO5204B(config)
    tek.open()
    tek.configure()
    for i in range(10):
        [wf, time] = tek.acquireWaveforms()
        print(len(time))
        sleep(0.1)

    #plt.plot(time, wf)
    #plt.show()



    tek.close()
    