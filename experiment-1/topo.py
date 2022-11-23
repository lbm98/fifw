#!/usr/bin/python

import sys
import time

from mininet.log import setLogLevel, info, error
from mininet.node import RemoteController

from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference

import matplotlib.pyplot as plt

NUMBER_OF_OBSERVATIONS = 50
TIME_BETWEEN_OBSERVATIONS = 0.2
SAVE_FIG_DIR = '/home/wifi/fifw/experiment-1'


def observe_dbm(sta):
    return sta.cmd('iw dev sta1-wlan0 link | grep signal | cut -d\  -f2')

def run_test(net, fading_cof):
    sta1 = net.get('sta1')

    # wait until we can observe dbm
    while True:
        if observe_dbm(sta1) != '':
            break

    # now we can observe dbm
    observations = []
    for _ in range(NUMBER_OF_OBSERVATIONS):
        dbm = int(observe_dbm(sta1))
        observations.append(dbm)
        time.sleep(TIME_BETWEEN_OBSERVATIONS)

    # visualize the data
    fig, ax = plt.subplots()
    ax.plot(range(NUMBER_OF_OBSERVATIONS), observations)
    # plt.show()
    fig.savefig(SAVE_FIG_DIR + f'/fading{fading_cof}')


def topology(args):
    if '-f' not in args:
        error('Please provide a fading coefficient with -f\n')
        return

    f_idx = args.index('-f')

    try:
        fading_cof_string = args[f_idx + 1]
    except IndexError:
        error('Please provide a value for the fading coefficient\n')
        return

    try:
        fading_cof  = int(fading_cof_string)
    except ValueError:
        error('Please provide an integer for the fading coefficient\n')
        return


    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference,
                       noise_th=-91, fading_cof=fading_cof)

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='a', channel='36',
                             position='15,30,0')
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.1/8',
                   position='10,20,0')
    c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    net.start()

    info("*** Running test\n")
    run_test(net, fading_cof)
    
    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
