## Create ports
#  set pwm_o [ create_bd_port -dir O pwm_o ]
#  set pwm_o1 [ create_bd_port -dir O pwm_o1 ]

## Create instance: redpitaya_converters_0, and set properties
add_ip_and_conf redpitaya_converters redpitaya_converters_0 {
	CLOCK_DUTY_CYCLE_STABILIZER_EN false }
connect_to_fpga_pins redpitaya_converters_0 phys_interface phys_interface_0


#######################################
#                                     #
# nco1 -> conv1 ----|                 #
#                    offset -> DAC A  #
#               |---|                 #
#          (A)--|                     #
# axi_to_dac                          #
#          (B)--|                     #
#               |---|                 #
#                    offset -> DAC B  #
# nco2 -> conv2 ----|                 #
#                                     #
#######################################

## Create instance: dds_ampl, and set properties
add_ip_and_conf axi_to_dac dds_ampl
connect_proc dds_ampl s00_axi 0x10000
connect_intf redpitaya_converters_0 clk_o dds_ampl ref_clk_i
connect_intf redpitaya_converters_0 rst_o dds_ampl ref_rst_i

## Create instance: nco_counter_1, and set properties
add_ip_and_conf nco_counter nco_counter_1 {
	COUNTER_SIZE 40 \
	LUT_SIZE 12 }
connect_proc nco_counter_1 s00_axi 0x70000
connect_intf redpitaya_converters_0 clk_o nco_counter_1 ref_clk_i
connect_intf redpitaya_converters_0 rst_o nco_counter_1 ref_rst_i

## Create instance: conv_nco_counter_1, and set properties
add_ip_and_conf convertComplexToReal conv_nco_counter_1 {
	DATA_SIZE 16 }
# nco_counter_1 -> conv_nco_counter_1
connect_intf nco_counter_1 sine_out conv_nco_counter_1 data_in

## Create instance: nco_counter_2, and set properties
add_ip_and_conf nco_counter nco_counter_2 {
	COUNTER_SIZE 40 \
	LUT_SIZE 12}
connect_proc nco_counter_2 s00_axi 0x80000
connect_intf redpitaya_converters_0 clk_o nco_counter_2 ref_clk_i
connect_intf redpitaya_converters_0 rst_o nco_counter_2 ref_rst_i

## Create instance: conv_nco_counter_2, and set properties
add_ip_and_conf convertComplexToReal conv_nco_counter_2 {
	DATA_SIZE 16 }
# nco_counter_2 -> conv_nco_counter_2
connect_intf nco_counter_2 sine_out conv_nco_counter_2 data_in

## Create instance: mixer_sin_1, and set properties
add_ip_and_conf multiplierReal mixer_sin_1 {
	DATA1_IN_SIZE 14 \
	DATA2_IN_SIZE 16 \
	DATA_OUT_SIZE 14}
# dds_ampl(A) -> mixer_sin_1(data1)
connect_intf dds_ampl dataA_out mixer_sin_1 data1_in
# conv_nco_counter_1(I) -> mixer_sin_1(data2)
connect_intf conv_nco_counter_1 dataI_out mixer_sin_1 data2_in

## Create instance: mixer_sin_2, and set properties
add_ip_and_conf multiplierReal mixer_sin_2 {
	DATA1_IN_SIZE 14 \
	DATA2_IN_SIZE 16 \
	DATA_OUT_SIZE 14}
# dds_ampl(B) -> mixer_sin_2(data1)
connect_intf dds_ampl dataB_out mixer_sin_2 data1_in
# conv_nco_counter_2(I) -> mixer_sin_2(data2)
connect_intf conv_nco_counter_2 dataI_out mixer_sin_2 data2_in

## Create instance: dds1_offset, and set properties
add_ip_and_conf add_constReal dds1_offset {
	DATA_IN_SIZE 14 \
	DATA_OUT_SIZE 14 }
connect_proc dds1_offset s00_axi 0x50000
# mixer_sin_1 -> dds1_offset
connect_intf mixer_sin_1 data_out dds1_offset data_in
# dds1_offset -> DAC A
connect_intf dds1_offset data_out redpitaya_converters_0 dataA_in

## Create instance: dds2_offset, and set properties
add_ip_and_conf add_constReal dds2_offset {
	DATA_IN_SIZE 14 \
	DATA_OUT_SIZE 14 }
connect_proc dds2_offset s00_axi 0x60000
# mixer_sin_2 -> dds2_offset
connect_intf mixer_sin_2 data_out dds2_offset data_in
# dds2_offset -> DAC B
connect_intf dds2_offset data_out redpitaya_converters_0 dataB_in


###################################################
#                                                 #
# nco3 -> conv3 ----|                             #
#                    mixer3 -> offset3 -|         #
#               |---|                   |         #
#          (A)--|                       |         #
# dds_ampl1                              data_pwm #
#          (B)--|                       |         #
#               |---|                   |         #
#                    mixer4 -> offset4 -|         #
# nco4 -> conv4 ----|                             #
#                                                 #
###################################################

## Create instance: dds_ampl1, and set properties
add_ip_and_conf axi_to_dac dds_ampl1 {
	DATA_SIZE 16 }
connect_proc dds_ampl1 s00_axi 0xC0000
connect_intf redpitaya_converters_0 clk_o dds_ampl1 ref_clk_i
connect_intf redpitaya_converters_0 rst_o dds_ampl1 ref_rst_i

## Create instance: nco_counter_3, and set properties
add_ip_and_conf nco_counter nco_counter_3 {
	COUNTER_SIZE 40 \
	LUT_SIZE 12 }
connect_proc nco_counter_3 s00_axi 0xD0000
connect_intf redpitaya_converters_0 clk_o nco_counter_3 ref_clk_i
connect_intf redpitaya_converters_0 rst_o nco_counter_3 ref_rst_i

## Create instance: conv_nco_counter_3, and set properties
add_ip_and_conf convertComplexToReal conv_nco_counter_3 {
	DATA_SIZE 16 }
# nco_counter_3 -> conv_nco_counter_3
connect_intf nco_counter_3 sine_out conv_nco_counter_3 data_in


## Create instance: nco_counter_4, and set properties
add_ip_and_conf nco_counter nco_counter_4 {
	COUNTER_SIZE 40 \
	LUT_SIZE 12 }
connect_proc nco_counter_4 s00_axi 0xE0000
connect_intf redpitaya_converters_0 clk_o nco_counter_4 ref_clk_i
connect_intf redpitaya_converters_0 rst_o nco_counter_4 ref_rst_i

## Create instance: conv_nco_counter_4, and set properties
add_ip_and_conf convertComplexToReal conv_nco_counter_4 {
	DATA_SIZE 16 }
# nco_counter_4 -> conv_nco_counter_4
connect_intf nco_counter_4 sine_out conv_nco_counter_4 data_in

## Create instance: mixer_sin_3, and set properties
add_ip_and_conf multiplierReal mixer_sin_3 {
	DATA1_IN_SIZE 16 \
	DATA2_IN_SIZE 16 \
	DATA_OUT_SIZE 16 }
# dds_ampl1(A) -> mixer_sin_3(data1)
connect_intf dds_ampl1 dataA_out mixer_sin_3 data1_in
# conv_nco_counter_3(I) -> mixer_sin_3(data2)
connect_intf conv_nco_counter_3 dataI_out mixer_sin_3 data2_in

## Create instance: mixer_sin_4, and set properties
add_ip_and_conf multiplierReal mixer_sin_4 {
	DATA1_IN_SIZE 16 \
	DATA2_IN_SIZE 16 \
	DATA_OUT_SIZE 16 }
# dds_ampl1(B) -> mixer_sin_4(data1)
connect_intf dds_ampl1 dataB_out mixer_sin_4 data1_in
# conv_nco_counter_4(I) -> mixer_sin_4(data2)
connect_intf conv_nco_counter_4 dataI_out mixer_sin_4 data2_in

## Create instance: dds3_offset, and set properties
add_ip_and_conf add_constReal dds3_offset {
	DATA_IN_SIZE 16 \
	DATA_OUT_SIZE 16 }
connect_proc dds3_offset s00_axi 0xA0000
# mixer_sin_3 -> dd3_offset
connect_intf mixer_sin_3 data_out dds3_offset data_in

## Create instance: dds4_offset, and set properties
add_ip_and_conf add_constReal dds4_offset {
	DATA_IN_SIZE 16 \
	DATA_OUT_SIZE 16 }
connect_proc dds4_offset s00_axi 0xB0000
# mixer_sin_4 -> dd4_offset
connect_intf mixer_sin_4 data_out dds4_offset data_in

## Create instance: data_pwm, and set properties
add_ip_and_conf dataReal_to_ram data_pwm {
	DATA_SIZE 16 \
	NB_INPUT 2 \
	NB_SAMPLE 2048 }
connect_proc data_pwm s00_axi 0xF0000
# dds3_offset -> data_pwm(data1)
connect_intf dds3_offset data_out data_pwm data1_in
# dds4_offset -> data_pwm(data2)
connect_intf dds4_offset data_out data_pwm data2_in


###################################################
#                                                 #
# ADCA -> adc1_offset -|                          #
#                      |                          #
#                       dataReal_to_ram_1         #
#                      |                          #
# ADCA -> adc1_offset -|                          #
#                                                 #
###################################################


## Create instance: adc1_offset, and set properties
add_ip_and_conf add_constReal adc1_offset {
	DATA_IN_SIZE 14 \
	DATA_OUT_SIZE 14 }
connect_proc adc1_offset s00_axi 0x20000
# adcA -> adc1_offset
connect_intf redpitaya_converters_0 dataA_out adc1_offset data_in

## Create instance: adc2_offset, and set properties
add_ip_and_conf add_constReal adc2_offset {
	DATA_IN_SIZE 14 \
	DATA_OUT_SIZE 14 }
connect_proc adc2_offset s00_axi 0x40000
# adcB -> adc2_offset
connect_intf redpitaya_converters_0 dataB_out adc2_offset data_in

## Create instance: dataReal_to_ram_1, and set properties
add_ip_and_conf dataReal_to_ram dataReal_to_ram_1 {
	DATA_SIZE 14 \
	NB_INPUT 2 \
	NB_SAMPLE 8192 }
connect_proc dataReal_to_ram_1 s00_axi 0x00000
# adc1_offset -> dataReal_to_ram_1(data1)
connect_intf adc1_offset data_out dataReal_to_ram_1 data1_in
# adc2_offset -> dataReal_to_ram_1(data2)
connect_intf adc2_offset data_out dataReal_to_ram_1 data2_in

###################################################
#                                                 #
# pwm_axi_0 ------------------------------------> #
#                                                 #
# pwm_axi_1 ------------------------------------> #
#                                                 #
###################################################

## Create instance: pwm_axi_0, and set properties
add_ip_and_conf pwm_axi pwm_axi_0 {
	COUNTER_SIZE 14 }
connect_intf redpitaya_converters_0 clk_o pwm_axi_0 ref_clk_i
connect_intf redpitaya_converters_0 rst_o pwm_axi_0 ref_rst_i
connect_proc pwm_axi_0 s00_axi 0x30000
connect_to_fpga_pins pwm_axi_0 pwm_o pwm_o

## Create instance: pwm_axi_1, and set properties
add_ip_and_conf pwm_axi pwm_axi_1 {
	COUNTER_SIZE 14 }
connect_intf redpitaya_converters_0 clk_o pwm_axi_1 ref_clk_i
connect_intf redpitaya_converters_0 rst_o pwm_axi_1 ref_rst_i
connect_proc pwm_axi_1 s00_axi 0x90000
connect_to_fpga_pins pwm_axi_1 pwm_o pwm_1

connect_proc_rst redpitaya_converters_0 adc_rst_i
