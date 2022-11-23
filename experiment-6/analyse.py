#!/usr/bin/python

import sys
import time


def main(filename):
    try:
        data = sys.stdin.read()
        dbm = data.split(" ")[1].strip()
    except:
        #dbm = 0
        return

    with open(filename, 'a') as fh:
        fh.write(f'{time.time()} {dbm}\n')



if __name__ == "__main__":
   main(sys.argv[1])