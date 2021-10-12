#!/usr/bin/env python
#IR 05.07.2021 added check of the Python interpreter version

import liboscimp_fpga
import sys

if sys.version_info[0]*10 + sys.version_info[1] >= 37 :
	liboscimp_fpga.fir_send_conf(sys.argv[1], sys.argv[2], 25)

else :
	liboscimp_fpga.fir_send_conf(sys.argv[1].encode('utf-8'), sys.argv[2].encode('utf-8'), 25)

