#!/usr/bin/env python

import liboscimp_fpga
import sys

liboscimp_fpga.fir_send_conf(sys.argv[1].encode('utf-8'), sys.argv[2].encode('utf-8'), 25)
