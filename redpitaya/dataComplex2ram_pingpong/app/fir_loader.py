#!/usr/bin/env python

import liboscimp_fpga
import sys

with open(sys.argv[2].encode('utf-8')) as f:
	coeff_nb = len(f.readlines())

liboscimp_fpga.fir_send_conf(sys.argv[1], sys.argv[2], coeff_nb)
