# Create instance: redpitaya_converters_12_0, and set properties
add_ip_and_conf redpitaya_converters_12 redpitaya_converters_12_0 {
	ADC_EN true\
	DAC_EN true }
connect_to_fpga_pins redpitaya_converters_12_0 phys_interface phys_interface_0
connect_proc redpitaya_converters_12_0 s00_axi 0x00000


###################################################
#                                                 #
# ADC A -> expanderReal_1 -> adc1_offset -> DAC A #
#                                                 #
# ADC B -> expanderReal_2 -> adcr2offset -> DAC B #
#                                                 #
###################################################

# Create instance: expanderReal_1, and set properties
add_ip_and_conf expanderReal expanderReal_1 {
    DATA_IN_SIZE {12} \
    DATA_OUT_SIZE {14} }

# Create instance: expanderReal_2, and set properties
add_ip_and_conf expanderReal expanderReal_2 {
    DATA_IN_SIZE {12} \
    DATA_OUT_SIZE {14} }

## Create instance: adc1_offset, and set properties
add_ip_and_conf add_constReal adc1_offset {
	DATA_IN_SIZE 14 \
	DATA_OUT_SIZE 14 }
connect_proc adc1_offset s00_axi 0x10000

## Create instance: adc2_offset, and set properties
add_ip_and_conf add_constReal adc2_offset {
	DATA_IN_SIZE 14 \
	DATA_OUT_SIZE 14 }
connect_proc adc2_offset s00_axi 0x20000

# ADC A -> expanderReal_1
connect_intf redpitaya_converters_12_0 dataA_out expanderReal_1 data_in
# expanderReal_1 -> adc1_offset
connect_intf expanderReal_1 data_out adc1_offset data_in
# adc1_offset -> DAC A
connect_intf adc1_offset data_out redpitaya_converters_12_0 dataA_in

# ADC B -> expanderReal_2
connect_intf redpitaya_converters_12_0 dataB_out expanderReal_2 data_in
# expanderReal_2 -> adc2_offset
connect_intf expanderReal_2 data_out adc2_offset data_in
# adc2_offset -> DAC B
connect_intf adc2_offset data_out redpitaya_converters_12_0 dataB_in

# redpitaya_converters_12 reset
connect_proc_rst redpitaya_converters_12_0 adc_rst_i
