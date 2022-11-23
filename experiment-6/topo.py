#!/usr/bin/python

import sys
import time

from mininet.log import setLogLevel, info
from mininet.node import RemoteController

from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference


# product should be 20
NUMBER_OF_OBSERVATIONS = 150
TIME_BETWEEN_OBSERVATIONS = 0.1


def observe_dbm(sta):
    comm = f''

    comm = (
        f'iw dev {sta.name}-wlan0 link'
        f' | grep signal'
        f' | python analyse.py {sta.name}.data'
    )
    return sta.cmd(comm)


def run_test(net):
    sta0 = net.get('sta0')

    open('sta0.data', 'w').close()

    for i in range(NUMBER_OF_OBSERVATIONS):
        observe_dbm(sta0)
        time.sleep(TIME_BETWEEN_OBSERVATIONS)


def topology(args):
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference,
                       noise_th=-91, fading_cof=3)

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid1', mode='a', channel='36',
                             position='60,150,0')
    ap2 = net.addAccessPoint('ap2', ssid='new-ssid2', mode='a', channel='36',
                             position='150,150,0')


    sta0 = net.addStation('sta0')

    net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    net.plotGraph(max_x=300, max_y=300)
    
    # start moving a bit later,
    # so the initial connection can be made
    net.startMobility(time=0)
    net.mobility(sta0, 'start', time=0, position='60,160,0')
    net.mobility(sta0, 'stop', time=20, position='150,160,0')
    net.stopMobility(time=20)

    # info('*** Creating links\n')
    # net.addLink(sta0, ap1)

    info("*** Starting network\n")
    net.start()
    # time.sleep(1) # give the network time to startup

    info("*** Running tests\n")
    run_test(net)
    # CLI(net)
    
    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
