import sys
import numpy as np
import h5py
import matplotlib.pyplot as plt


if __name__ == '__main__':
    runnumber = int(sys.argv[1])

    #create new h5py file
    fname = 'run' + str(runnumber) + '.hdf5'
    print('Opening: ', fname, '\n')
    hdf = h5py.File(fname, 'r')
    print('Timestamp: ', hdf.attrs['timestamp'])

    #group tctdata:
    tctdata = hdf['tctdata']
    print('Diamond Name: ', tctdata.attrs['diamond_name'])
    print('Bias Voltage: ', tctdata.attrs['bias_voltage'])
    print('Number of waveforms: ', tctdata.attrs['number_of_waveforms'])
    print('Laser Pulse Energy: ', tctdata.attrs['laser_pulse_energy'])
    print('Diamond Side: ', tctdata.attrs['side'])
    print('Amplifier: ', tctdata.attrs['amplifier'])
    print('PCB: ', tctdata.attrs['pcb'])
    print('Comments:\n', tctdata.attrs['comments'], '\n')

    #check how to get total number of datasets
    for idx in range(0,6):
        i = str(idx)
        timestamp = tctdata[i].attrs['timestamp'] #single array, serves all wfs in data as time axis
        x = tctdata[i].attrs['x']
        y = tctdata[i].attrs['y']
        z = tctdata[i].attrs['z']
        time_axis = tctdata[i].attrs['time_axis']
        data = tctdata[i]
        larr = len(time_axis)
        plt.plot(time_axis, data[larr*idx:larr*(idx+1)])
    plt.show()


    hdf.close()


