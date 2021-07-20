BASE_NAME=double_iq_pid_vco
CORE_MODULES_LIST = \
	${OSCIMP_DIGITAL_DRIVER}/add_const_core/add_const_core.ko \
	${OSCIMP_DIGITAL_DRIVER}/data_to_ram_core/data_to_ram_core.ko \
	${OSCIMP_DIGITAL_DRIVER}/fpgagen_core/fpgagen_core.ko \
	${OSCIMP_DIGITAL_DRIVER}/axi_to_dac_core/axi_to_dac_core.ko \
	${OSCIMP_DIGITAL_DRIVER}/pidv3_axi_core/pidv3_axi_core.ko \
	${OSCIMP_DIGITAL_DRIVER}/nco_counter_core/nco_counter_core.ko \
	${OSCIMP_DIGITAL_DRIVER}/fir_core/fir_core.ko

SUPP_FILE = fir_loader.py zmq_data2ram_slow.py \
	zmq_data2ram_fast.py fir_lp_4000000_12000000_40dB.dat

ifeq ($(BOARD_NAME), redpitaya)
SUPP_FILE += double_iq_pid_vco_webserver14.py
endif
ifeq ($(BOARD_NAME), redpitaya16)
SUPP_FILE += double_iq_pid_vco_webserver16.py
endif
include $(OSCIMP_DIGITAL_APP)/Makefile.inc
