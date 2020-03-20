#!/usr/bin/env python

import liboscimp_fpga
import sys

#liboscimp_fpga.fir16bits_send_conf('/dev/demod_fir'.encode('utf-8'), sys.argv[1].encode('utf-8'), 55)
liboscimp_fpga.fir_MultiSend_confSigned('/dev/demod_fir'.encode('utf-8'), 1, sys.argv[1].encode('utf-8'), 55)
