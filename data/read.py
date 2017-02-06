import sys
import numpy as np
import h5py

#isFile    = isinstance(item, h5py.File)
#isGroup   = isinstance(item, h5py.Group)
#isDataset = isinstance(item, h5py.Dataset)



if __name__ == '__main__':
    runnumber = int(sys.argv[1])

    #create new h5py file
    fname = 'run' + str(runnumber) + ".hdf5"
    print('Opening: ', fname)
    hdf = h5py.File(fname, "r")
    print("Timestamp: ", hdf.attrs['timestamp'])

    tctdata = hdf['tctdata']
    print("Diamond Name: ", tctdata.attrs['diamond_name'])
    print("Diamond Side: ", tctdata.attrs['side'])
    print("Bias Voltage: ", tctdata.attrs['bias_voltage'])
    print("Laser Pulse Energy: ", tctdata.attrs['laser_pulse_energy'])
    time_array = tctdata.attrs['time_array']
    #print(time_array)
    data1 = tctdata['1']
    print(data1)
    hdf.close()


