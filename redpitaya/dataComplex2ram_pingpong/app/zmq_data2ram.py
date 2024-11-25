#!/usr/bin/env python

import zmq, time
import sys

port = int(sys.argv[2].encode('utf-8'))

DATA_SIZE = int(sys.argv[3].encode('utf-8'))
NB_INPUT = int(sys.argv[4].encode('utf-8'))
NB_SAMPLE = int(sys.argv[5].encode('utf-8'))

context = zmq.Context()
sock = context.socket(zmq.PUB)
sock.bind(f"tcp://*:{port}")

while True:
    time.sleep(0.1)
    with open(sys.argv[1].encode('utf-8'), 'rb') as f:
        sock.send(f.read(NB_INPUT*NB_SAMPLE*((DATA_SIZE-1)//8+1)))
