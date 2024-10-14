import datetime
import numpy as np
import h5py


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
        self.sample_name = self.config['AcquisitionControl']['sample_name']
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
        self.tctdata.attrs['sample_name'] = self.sample_name
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
    def setSampleName(self, val):
        self.sample_name = val
        self.config['AcquisitionControl']['sample_name'] = val
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