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
    time_axis = tctdata['0'].attrs['time_axis']
    larr = len(time_axis)

    for idx in range(0,400):
        #gets the data from one scanpoint, there are multiple wf per scanpoint
        i = str(idx)
        timestamp = tctdata[i].attrs['timestamp']
        x = tctdata[i].attrs['x']
        y = tctdata[i].attrs['y']
        z = tctdata[i].attrs['z']
        data = tctdata[i]

        nw = int(len(data)/larr)
        res = []
        for wf in range(nw):
            ped = np.sum(data[wf*larr:wf*larr+1000])
            sig = np.sum(data[wf*larr+1000:wf*larr+2000])
            res.append(sig - ped)

        mres = np.mean(res)
        mstd = np.std(res)
        print(idx, mres, mstd)








        plt.plot(time_axis, data[larr*idx:larr*(idx+1)])
    plt.show()
    

    hdf.close()


