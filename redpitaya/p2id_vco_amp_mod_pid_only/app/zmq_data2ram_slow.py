#!/usr/bin/env python

import zmq, time

context = zmq.Context()
sock = context.socket(zmq.PUB)
sock.bind("tcp://*:9902")

while True:
    time.sleep(0.05)
    with open('/dev/data_slow', 'rb') as f:
        sock.send(f.read(8192))
