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
    
    def __init__(self, resource):
        # Configure VISA resource
        self.rm = visa.ResourceManager()
        self.inst = self.rm.open_resource(resource) 
        
        print('Connected to: ', self.inst.ask('*idn?'))
        self.inst.write('*rst')  #default the instrument

        #FIXME: get from config file: variables for individual settings
        self.horizscale = '20e-9'      #sec/div
        self.samplerate = '10e9'       #S/sec
        self.numberofframes = 50
        self.voltsperdiv = .5
        self.position = -3
        self.highthresh = 2
        self.lowthresh = 0.75
        self.trig_level = 1
        
        #class variables for data processing
        self.yoffset = 0
        self.ymult = 0
        self.yzero = 0
        self.numberofpoints = 0
        self.xincrement = 0
        self.xzero = 0


    def configure(self):
        #configure general settings and channels
        self.inst.write('acquire:state 0')                                          #turn off the acquisition system
        self.inst.write('horizontal:mode auto')                                     #set horizontal settings to auto
        self.inst.write('horizontal:mode:scale {0}'.format(self.horizscale))        #set horiztonal scale
        self.inst.write('horizontal:mode:samplerate {0}'.format(self.samplerate))   #set sample rate
        self.inst.write('acquire:mode sample')                                      #set acquire mode to sample
        self.inst.write('horizontal:fastframe:state 1')                             #turn on FastFrame
        self.inst.write('horizontal:fastframe:count {0}'.format(self.numberofframes))   #specify number of frames
        self.inst.write('ch1:scale {0}'.format(self.voltsperdiv))                       #set vertical scale
        self.inst.write('ch1:position {0}'.format(self.position))                       #set vertical position
        print('Channel settings configured.')
        
        #configure triggering:
        self.inst.write('trigger:a:type edge')                                  #set trigger type to pulse
        self.inst.write('trigger:a:mode normal')                                #set trigger mode to normal
        self.inst.write('trigger:a:edge:coupling dc')                           #couple dc
        self.inst.write('trigger:a:edge:slope rise')                            #rising edge triggering
        self.inst.write('trigger:a:edge:source ch2')                            #set trigger channel
        self.inst.write('trigger:a:level:ch2 {0}'.format(self.trig_level))      #set trigger level
        self.inst.write('trigger:a:level:ch2 1')                                #set trigger level voltage
        print('Trigger settings configured.')
        
        ## Configure data transfer settings
        self.inst.write('header 0')                    #turn the header off
        self.inst.write('horizontal:fastframe:sumframe none') #tell the scope to create a summary frame that is the average of all frames
        self.inst.write('data:encdg fastest')          #set encoding type to fast binary
        self.inst.write('data:source ch1')             #set data source
        self.inst.write('data:stop 100000')            #set end of record
        self.inst.write('wfmoutpre:byt_n 1')           #set number of bytes per data point
        self.inst.write('data:framestart 1')           #as long as start/stop frames are greater than the total number of frames,
        self.inst.write('data:framestop 1000')         #the program will only capture the last frame, which is the summary frame, which is what we want
        print('Data transfer settings configured.')

        #vertical data
        self.yoffset = float(self.inst.ask('wfmoutpre:yoff?'))   #yoffset is unscaled offset data that is set by the ch<x>:offset
        self.ymult = float(self.inst.ask('wfmoutpre:ymult?'))    #ymult is the scaling factor that is set by ch<x>:scale
        self.yzero = float(self.inst.ask('wfmoutpre:yzero?'))    #yzero is scaled position data that is set by ch<x>:position

        #horizontal data
        self.numberofpoints = int(self.inst.ask('wfmoutpre:nr_pt?'))     #number of points in the waveform acquisition
        self.xincrement = float(self.inst.ask('wfmoutpre:xincr?'))       #amount of time between data points
        self.xzero = float(self.inst.ask('wfmoutpre:xzero?'))            #absolute time value of the beginning of the waveform record
    
    
    def acquireWaveforms(self):
        self.inst.Timeout = 60
        self.inst.write('acquire:stopafter sequence')  #set scope to single acquisition mode
        self.inst.write('acquire:state 1')             #start acquisition 
        done = 0
        while(done != 1):                              #wait until scope has finished acquiring waveforms
            try:
                done = int(self.inst.ask('*opc?'))
            except:
                sleep(0.15)                        
        
        
        self.inst.write('curve?')
        rawdata = self.inst.read_raw()


        headerlength = len(rawdata)%100 - 1 #determining the length of the header (dirty fix)
        #header = rawdata[:headerlength]     #header for later use?
        rawdata = rawdata[headerlength:-1]  #strip the header
        data = numpy.array(unpack('{0}b'.format(self.numberofpoints*self.numberofframes), rawdata))             #unpack data to numpy array
        scaleddata = (data-self.yoffset)*self.ymult+self.yzero                                                  #scale data to volts
        scaledtime = numpy.arange(self.xzero,self.xzero+(self.xincrement*self.numberofpoints),self.xincrement)  #always the same time
        print('Waveforms acquired.\n')
        return (scaleddata, scaledtime)


    def close(self):
        self.inst.close()


    
