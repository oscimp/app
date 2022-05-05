#!/usr/bin/env python

import zmq, time

context = zmq.Context()
sock1 = context.socket(zmq.PUB)
sock1.bind("tcp://*:9901")
sock2 = context.socket(zmq.PUB)
sock2.bind("tcp://*:9902")

while True:
    time.sleep(0.05)
    with open('/dev/dataComplex_to_ram_0', 'rb') as f1:
        sock1.send(f1.read(16384*2*2))
    with open('/dev/dataComplex_to_ram_1', 'rb') as f2:
        sock2.send(f2.read(16384*2*2))
