##Simple GUI-based DAQ system for a edge-TCT setup.

The software allows to collect waveforms at certain positions and perform 3D scans of the sample with live monitoring. Also knive-edge scans of the laser beam are possible. The data is saved as numpy arrays in a hdf5 file.

###Hardware:
- Newport ESP301 Controller with 3 stages:
	- M-ILS150CC stage
	- M-ILS100CC stage
	- M-VP-5ZA stage
- Tektronix DPO5204B 2GHz

###Software Requirements:
- Python3 (ConfigObj, PyQt5, numpy, matplotlib, pyserial)
- Qt5
- NI VISA

###Use:
After all packages were installed the software can be easily started with:
python main.py







