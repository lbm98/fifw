#!/usr/bin/python

import sys
import time

from mininet.log import setLogLevel, info, error
from mininet.node import RemoteController

from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference

NUMBER_OF_OBSERVATIONS = 200
TIME_BETWEEN_OBSERVATIONS = 0.05


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

    # store the observations for later analysis
    with open(f'fading{fading_cof}.data', 'w') as fh:
        for obs in observations:
            fh.write(f'{obs}\n')


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
                             position='150,150,0')
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.1/8',
                   position='150,150,0')
    c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    if '-p' in args:
        net.plotGraph(max_x=300, max_y=300)

    # https://github.com/intrig-unicamp/mininet-wifi/blob/master/examples/mobility.py
    net.startMobility(time=0)
    net.mobility(sta1, 'start', time=0, position='150,149,0')
    net.mobility(sta1, 'stop', time=20, position='150,100,0')
    net.stopMobility(time=20)

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
