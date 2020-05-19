import subprocess
from time import sleep


def main():
	while True:
		result = subprocess.run(['lsof', '-t', '/dev/ttyACM1'], stdout=subprocess.PIPE)
		procid = int(result.stdout.decode('utf-8').split('\n')[0])
		if procid != 17588:
			print('Procid: ', procid)
			break
		sleep(0.1)





if __name__ == '__main__':
	main()