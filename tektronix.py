####################################               
# Author: Christian Dorfer
# Email: cdorfer@phys.ethz.ch                                  
####################################

import visa
import numpy
from struct import unpack
from time import sleep
import socket


class TektronixMSO5204B(object):
    """ Readout class for the MSO5204 Oscilloscope.
    :Usage: 
    >>> tek = TektronixMSO5204('TCPIP0::192.168.1.111::inst0::INSTR') # open communication with the scope
    """

    #fixme: select channel upon selecting scan type
    #CH1: Diamond
    #CH2: Trigger
    #CH3: Diode

    def __init__(self, conf):
        self.config = conf
        self.rm = None
        self.inst = None
        self.scan_type = 'regular'

        #from config file:
        self.resource = 0
        self.horizscale = 0
        self.samplerate = 0
        self.numberofwf = 0
        self.voltsperdiv = 0
        self.ch1_offset = 0
        self.ch2_trig_level =  0
        self.ch1_termination = 0
        self.ch2_termination = 0
        self.samplesInWf = 2000 #default, updated from config
        
        self.readConfig()


        #class variables for data processing
        self.yoffset = 0
        self.ymult = 0
        self.yzero = 0
        self.numberofpoints = 0
        self.xincrement = 0
        self.xzero = 0


    def open(self):
        #configure VISA resource
        self.rm = visa.ResourceManager('@py')
        self.inst = self.rm.open_resource(self.resource) 
        self.inst.Timeout = 60

        print('Connected to: ', self.inst.ask('*idn?').rstrip())
        self.inst.write('*rst')  #default the instrument


    def readConfig(self):
        self.scan_type = self.config['AcquisitionControl']['scan_type']

        if self.scan_type == 'knife_edge':
            tekConfig = 'TektronixDiode'

        if self.scan_type == 'regular':
            tekConfig = 'TektronixDiamond'

        self.resource = self.config[tekConfig]['address']
        self.horizscale = self.config[tekConfig]['horizscale']  #sec/div
        self.samplerate = self.config[tekConfig]['samplerate']  #S/sec
        self.numberofwf = int(self.config['AcquisitionControl']['number_of_waveforms'])
        self.voltsperdiv = float(self.config[tekConfig]['voltsperdiv'])
        self.ch1_offset = float(self.config[tekConfig]['ch1_offset'])
        self.ch2_trig_level =  float(self.config[tekConfig]['ch2_trig_level'])
        self.ch1_termination = int(self.config[tekConfig]['ch1_termination'])
        self.ch2_termination = int(self.config[tekConfig]['ch2_termination'])
        self.samplesInWf = int(self.config[tekConfig]['samples_in_wf'])
        print(self.samplesInWf)

    #gui interface to select different oscilloscope configurations
    def setScanType(self, scantype):
        self.scan_type = scantype
        self.readConfig()


    def configure(self):
        #update number of waveforms to be acquired
        self.numberofwf = int(self.config['AcquisitionControl']['number_of_waveforms'])

        #configure general settings and channels
        self.inst.write('acquire:state 0')                                          #turn off the acquisition system
        self.inst.write('horizontal:mode auto')                                     #set horizontal settings to auto
        self.inst.write('horizontal:mode:scale {0}'.format(self.horizscale))        #set horiztonal scale
        self.inst.write('horizontal:mode:samplerate {0}'.format(self.samplerate))   #set sample rate
        self.inst.write('acquire:mode sample')                                      #set acquire mode to sample
        self.inst.write('horizontal:fastframe:state 1')                             #turn on FastFrame
        self.inst.write('horizontal:fastframe:count {0}'.format(self.numberofwf))   #specify number of frames
        
        if self.scan_type == 'knife_edge':
            self.inst.write('data:source ch3')                                          #set data source
            self.inst.write('ch3:scale {0}'.format(self.voltsperdiv))                   #set vertical scale
            self.inst.write('ch3:offset {0}'.format(self.ch1_offset))                   #set vertical position
            self.inst.write('ch3:termination {0}'.format(self.ch1_termination))         #set channel 1 termination
            self.inst.write('ch3:coupling ac')						                    #set channel 1 coupling  
            self.inst.write('select:ch1 OFF')                                           #this is stupid, but necessary
            self.inst.write('select:ch3 ON')                                            #this is stupid, but necessary

        if self.scan_type == 'regular':
            self.inst.write('data:source ch1')
            self.inst.write('ch1:scale {0}'.format(self.voltsperdiv))                   #set vertical scale (CH3 for knive edge scan (same as ch1))
            self.inst.write('ch1:offset {0}'.format(self.ch1_offset))                   #set vertical position (CH3 for knive edge scan (same as ch1))
            self.inst.write('ch1:termination {0}'.format(self.ch1_termination))         #set channel 1 termination (CH3 for knive edge scan (same as ch1))
            self.inst.write('ch1:coupling ac')                                          #set channel 1 coupling (CH3 for knive edge scan (same as ch1))
            self.inst.write('select:ch3 OFF')                                           #this is stupid, but necessary
            self.inst.write('select:ch1 ON')                                            #this is stupid, but necessary

        
        #configure triggering on CH2:
        self.inst.write('select:ch2 ON')
        self.inst.write('ch2:termination {0}'.format(self.ch2_termination))     #set channel 2 termination (trigger channel)
        self.inst.write('trigger:a:type edge')                                  #set trigger type to pulse
        self.inst.write('trigger:a:mode normal')                                #set trigger mode to normal
        self.inst.write('trigger:a:edge:coupling dc')                           #couple dc
        self.inst.write('trigger:a:edge:slope rise')                            #rising edge triggering
        self.inst.write('trigger:a:edge:source ch2')                            #set trigger channel
        self.inst.write('trigger:a:level:ch2 {0}'.format(self.ch2_trig_level))  #set trigger level
        self.inst.write('trigger:a:level:ch2 1')                                #set trigger level voltage
        #print('Trigger settings configured.')
        
        
        self.inst.write('data:encdg fastest')                   #set encoding type to fast binary
        self.inst.write('wfmoutpre:byt_n 1')                    #set number of bytes per data point
        
        self.inst.write('data:start 1')                         #transfer from the first data point of the first waveform
        self.inst.write('data:stop {0}'.format(self.samplesInWf))

        self.inst.write('header 0')                             #turn the header off
        self.inst.write('horizontal:fastframe:sumframe none')   #tell the scope not to create a summary frame that is the average of all frames

        self.inst.write('data:framestart 1')           #as long as start/stop frames are greater than the total number of frames,
        #self.inst.write('data:framestop 2000')         #the program will only capture the last frame, which is the summary frame, which is what we want
        self.inst.write('data:framestop {0}'.format(self.samplesInWf))
        #print('Data transfer settings configured.')

        #vertical data
        self.yoffset = float(self.inst.ask('wfmoutpre:yoff?'))   #yoffset is unscaled offset data that is set by the ch<x>:offset
        self.ymult = float(self.inst.ask('wfmoutpre:ymult?'))    #ymult is the scaling factor that is set by ch<x>:scale
        self.yzero = float(self.inst.ask('wfmoutpre:yzero?'))    #yzero is scaled position data that is set by ch<x>:position

        #horizontal data
        self.numberofpoints = int(self.inst.ask('wfmoutpre:nr_pt?'))     #number of points in the waveform acquisition
        print("We take: " + str(self.numberofpoints) + " data points in each wf!")
        self.xincrement = float(self.inst.ask('wfmoutpre:xincr?'))       #amount of time between data points
        self.xzero = float(self.inst.ask('wfmoutpre:xzero?'))            #absolute time value of the beginning of the waveform record
        print("Data channel:", self.inst.ask('data:source?'))
        print("Tektronix DPO5204B configured!")

    
    def acquireWaveforms(self):
        self.inst.write('acquire:stopafter sequence')  #set scope to single acquisition mode
        self.inst.write('acquire:state 1')             #start acquisition 

        done = 0
        while(done != 1):                              #wait until scope has finished acquiring waveforms
            try:
                done = int(self.inst.ask('*opc?'))
            except:
                sleep(0.01)                        

        self.inst.write('curve?')
        rawdata = self.inst.read_raw()

        headerlength = len(rawdata)%100 - 1 #determining the length of the header (dirty fix)
        #header = rawdata[:headerlength]     #header for later use?
        rawdata = rawdata[headerlength:-1]  #strip the header

        #format string gives (size of array)b - where b is the unsigned char, osci data is only 8 bit but 32 bit is faster in the CPU?
        data = numpy.array(unpack('{0}b'.format(self.numberofpoints*self.numberofwf), rawdata), dtype=numpy.int32)  #unpack data to numpy array
        scaleddata = (data-self.yoffset)*self.ymult+self.yzero
        #scale data to volts
        #scaledtime = numpy.arange(self.xzero,self.xzero+(self.xincrement*self.numberofpoints),self.xincrement)  #always the same time
        scaledtime = numpy.arange(self.xzero,(self.xincrement*self.numberofpoints),self.xincrement) #it gave 1 point too much
        #print('Waveforms acquired.')
        return (scaleddata.astype(numpy.float32), scaledtime.astype(numpy.float32)[0:self.samplesInWf])


    def reset(self):
        #reset to normal working mode
        self.inst.write('horizontal:fastframe:state 0') #turn  FastFrame off
        self.inst.write('acquire:state 1') 



    def close(self):
        if(self.inst):
            self.inst.close()
            self.rm = None
            self.inst = None
            print("Connection to DPO5204B closed.")


    
