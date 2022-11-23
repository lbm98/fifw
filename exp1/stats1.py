import time
import subprocess
import matplotlib.pyplot as plt


MW_RUN = '/home/wifi/mininet-wifi/util/m'


def observe():
	dbm = subprocess.check_output(
		f'{MW_RUN} sta1 iw dev sta1-wlan0 link | grep signal | cut -d\  -f2',
		shell=True
	)
	dbm = int(dbm)
	
	return dbm


def main():
	n_observations = 20
	time_step = 0.5
	
	x = range(n_observations)
	y = []
	for i in range(n_observations):
		y.append(observe())
		time.sleep(time_step)
	
	fig, ax = plt.subplots()
	ax.plot(x, y)
	plt.show()


if __name__ == '__main__':
	main()
