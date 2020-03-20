#!/usr/bin/env python

import time, struct, liboscimp_fpga

liboscimp_fpga.fpgagen_send_conf("/dev/pwm_dac".encode("utf-8"), 1<<2, 1)
liboscimp_fpga.fpgagen_send_conf("/dev/pwm_dac".encode("utf-8"), 2<<2, 50000) 
liboscimp_fpga.fpgagen_send_conf("/dev/pwm_dac".encode("utf-8"), 3<<2, 100000)
liboscimp_fpga.fpgagen_send_conf("/dev/pwm_dac".encode("utf-8"), 4<<2, 1)

while True:
    time.sleep(0.1)
    with open('/dev/data_pwm', 'rb') as f:
        message = list(struct.unpack('4096h'.encode('utf-8'), f.read(8192)))
        val = (sum(message[0::2])/len(message[0::2])+10000)*100000/10000/2*1+1
#        print(val)
        liboscimp_fpga.fpgagen_send_conf("/dev/pwm_dac".encode("utf-8"), 2<<2, int(val))
