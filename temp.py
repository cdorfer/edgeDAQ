import serial
from time import sleep, time
import sys
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from shutter import Shutter


plotting = False



def main():
	shut = Shutter()
	t0 = time()
	t = []
	temp = []

	file = open("temp_out.txt", "w")

	if plotting:
		plt.ion()


	while(True):
		val = shut.getTemperature()
		print(val)
		now = time()

		t.append(now-t0)
		temp.append(val)

		data = str(time()) + ',' + str(t[-1]) + ',' + str(temp[-1]) + '\n' 
		file.write(data)
		file.flush()

		if plotting:
			plt.plot(t, temp, 'r+', markersize=1)
			plt.show()
			plt.pause(0.005)
		
		sleep(1)


if __name__ == '__main__':
	try: 
		main()
	except KeyboardInterrupt:
		raise SystemExit
