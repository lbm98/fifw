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

"""Observes throughput in bytes per second"""
def observe_throughput(server_sta, client_sta):

    # transmit for 1 second (-t1)
    # present report results in CSV (-yC)
    data = client_sta.cmd(f'iperf -c {server_sta.IP()} -yC -t5')
    # the throughput is the last value in the CSV list
    return data.split(',')[-1].strip()


def store_observations(observations):
    with open(f'yyy.data', 'w') as fh:
        for obs in observations:
            fh.write(f'{obs}\n')


def run_test(net):
    sta0 = net.get('sta0')
    sta1 = net.get('sta1')
    sta2 = net.get('sta2')
    sta3 = net.get('sta3')

    sta0.cmd('iperf -s &')
    time.sleep(2)

    observations = []
    for i in range(10):
        obs = observe_throughput(sta0, sta1)
        observations.append(obs)

    store_observations(observations)

    sta0.cmd('kill iperf')


def topology(args):
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference,
                       noise_th=-91, fading_cof=3)

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='a', channel='36',
                             position='150,150,0')


    net.addStation('sta0', position='130,170,0')
    net.addStation('sta1', position='130,130,0')
    net.addStation('sta2', position='170,130,0')
    net.addStation('sta3', position='170,170,0')

    #server1 = net.addHost('server1', ip='10.0.0.100/8')

    c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    if '-p' in args:
        net.plotGraph(max_x=300, max_y=300)

    info("*** Starting network\n")
    net.start()
    time.sleep(1)

    info("*** Running test\n")
    run_test(net)
    # CLI(net)
    
    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
