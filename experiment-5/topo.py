#!/usr/bin/python

import sys
import time

from mininet.log import setLogLevel, info
from mininet.node import RemoteController

from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference


TIME_TO_RUN_IPERF = 1 # seconds
NUMBER_OF_OBSERVATIONS = 8


def observe_dbm(sta):
    comm = (
        f'iw dev sta1-wlan0 link'
        f' | grep signal'
        f' | cut -d " " -f2'
        f' &' # make it a background task
    )
    return sta.cmd(comm)


"""Observes throughput in bytes per second"""
def observe_throughput(server_sta, client_sta):

    # transmit for 1 second (-t1)
    # present report results in CSV (-yC)
    comm = (
        f'iperf -c {server_sta.IP()} -yC -t{TIME_TO_RUN_IPERF}'
        f' | cut -d "," -f8'
        f' >> {client_sta.name}.data'
        f' &' # make it a background task
    )
    client_sta.cmd(comm)


def run_test(net):
    sta0 = net.get('sta0')
    sta1 = net.get('sta1')
    sta2 = net.get('sta2')
    sta3 = net.get('sta3')

    sta0.cmd('iperf -s &')
    # give iperf time to startup
    # since a background task returns immediately
    time.sleep(2)

    open('sta1.data', 'w').close()
    open('sta2.data', 'w').close()
    open('sta3.data', 'w').close()

    for i in range(NUMBER_OF_OBSERVATIONS):
        observe_throughput(sta0, sta1)
        time.sleep(TIME_TO_RUN_IPERF + 0.2)
        # assume that after the sleep,
        # the iperf client task is finished
        # note the small leeway

    
    for i in range(NUMBER_OF_OBSERVATIONS):
        observe_throughput(sta0, sta1)
        observe_throughput(sta0, sta2)
        time.sleep(TIME_TO_RUN_IPERF + 0.2)
    
    for i in range(NUMBER_OF_OBSERVATIONS):
        observe_throughput(sta0, sta1)
        observe_throughput(sta0, sta2)
        observe_throughput(sta0, sta3)
        time.sleep(TIME_TO_RUN_IPERF + 0.2)

    # cleanup background task
    sta0.cmd('pkill iperf')


def topology(args):
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference,
                       noise_th=-91, fading_cof=3)

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='a', channel='36',
                             position='150,150,0')


    sta0 = net.addStation('sta0', position='130,170,0')
    sta1 = net.addStation('sta1', position='130,130,0')
    sta2 = net.addStation('sta2', position='170,130,0')
    sta3 = net.addStation('sta3', position='170,170,0')

    net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    if '-p' in args:
        net.plotGraph(max_x=300, max_y=300)

    info('*** Creating links\n')
    net.addLink(sta0, ap1)
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)
    net.addLink(sta3, ap1)

    info("*** Starting network\n")
    net.start()
    time.sleep(1) # give the network time to startup

    info("*** Running tests\n")
    # run_test(net)
    CLI(net)
    
    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
