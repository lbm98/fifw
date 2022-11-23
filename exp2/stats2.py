import time
import subprocess
import matplotlib.pyplot as plt

# Edit this to your machine environment
MN_EXE = '/home/wifi/mininet-wifi/util/m'

# Edit this as you wish
N_OBSERVATIONS = 200
TIME_BETWEEN_OBSERVATIONS = 0.05


def mn_run(command):
	return subprocess.check_output(
		f'{MN_EXE} {command}',
		shell=True
	)

def observe_dbm():
	dbm = mn_run('sta1 iw dev sta1-wlan0 link | grep signal | cut -d\  -f2')
	if dbm == b'':
		return 0
	return int(dbm)


def main():
	x = range(N_OBSERVATIONS)
	y = []
	for i in range(N_OBSERVATIONS):
		y.append(observe_dbm())
		time.sleep(TIME_BETWEEN_OBSERVATIONS)
	
	fig, ax = plt.subplots()
	ax.plot(x, y)
	plt.show()


if __name__ == '__main__':
	main()
