#!/usr/bin/env python

import liboscimp_fpga
import sys

liboscimp_fpga.fir_send_conf(sys.argv[1], sys.argv[2], 25)
