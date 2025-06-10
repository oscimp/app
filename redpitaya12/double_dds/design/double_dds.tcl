add_ip_and_conf redpitaya_converters_12 redpitaya_converters_12_0 {}
connect_proc redpitaya_converters_12_0 s00_axi 0x00000
connect_to_fpga_pins redpitaya_converters_12_0 phys_interface phys_interface_0
connect_proc_rst redpitaya_converters_12_0 adc_rst_i

add_ip_and_conf axi_to_dac dds_ampl
connect_proc dds_ampl s00_axi 0x10000
connect_intf redpitaya_converters_12_0 clk_o dds_ampl ref_clk_i
connect_intf redpitaya_converters_12_0 rst_o dds_ampl ref_rst_i

add_ip_and_conf nco_counter nco_counter_1 {
	COUNTER_SIZE 40 \
	LUT_SIZE 12 }
connect_proc nco_counter_1 s00_axi 0x20000
connect_intf redpitaya_converters_12_0 clk_o nco_counter_1 ref_clk_i
connect_intf redpitaya_converters_12_0 rst_o nco_counter_1 ref_rst_i

add_ip_and_conf convertComplexToReal conv_nco_counter_1 {
	DATA_SIZE 16 }
connect_intf nco_counter_1 sine_out conv_nco_counter_1 data_in

add_ip_and_conf nco_counter nco_counter_2 {
	COUNTER_SIZE 40 \
	LUT_SIZE 12}
connect_proc nco_counter_2 s00_axi 0x30000
connect_intf redpitaya_converters_12_0 clk_o nco_counter_2 ref_clk_i
connect_intf redpitaya_converters_12_0 rst_o nco_counter_2 ref_rst_i

add_ip_and_conf convertComplexToReal conv_nco_counter_2 {
	DATA_SIZE 16 }
connect_intf nco_counter_2 sine_out conv_nco_counter_2 data_in

add_ip_and_conf multiplierReal mixer_sin_1 {
	DATA1_IN_SIZE 14 \
	DATA2_IN_SIZE 16 \
	DATA_OUT_SIZE 14}
connect_intf dds_ampl dataA_out mixer_sin_1 data1_in
connect_intf conv_nco_counter_1 dataI_out mixer_sin_1 data2_in

add_ip_and_conf multiplierReal mixer_sin_2 {
	DATA1_IN_SIZE 14 \
	DATA2_IN_SIZE 16 \
	DATA_OUT_SIZE 14}
connect_intf dds_ampl dataB_out mixer_sin_2 data1_in
connect_intf conv_nco_counter_2 dataI_out mixer_sin_2 data2_in

add_ip_and_conf add_constReal dds1_offset {
	DATA_IN_SIZE 14 \
	DATA_OUT_SIZE 14 }
connect_proc dds1_offset s00_axi 0x40000
connect_intf mixer_sin_1 data_out dds1_offset data_in

connect_intf dds1_offset data_out redpitaya_converters_12_0 dataA_in

add_ip_and_conf add_constReal dds2_offset {
	DATA_IN_SIZE 14 \
	DATA_OUT_SIZE 14 }
connect_proc dds2_offset s00_axi 0x50000
connect_intf mixer_sin_2 data_out dds2_offset data_in

connect_intf dds2_offset data_out redpitaya_converters_12_0 dataB_in

#ADC

add_ip_and_conf add_constReal adc1_offset {
	DATA_IN_SIZE 12 \
	DATA_OUT_SIZE 16 }
connect_proc adc1_offset s00_axi 0x60000
connect_intf redpitaya_converters_12_0 dataA_out adc1_offset data_in

add_ip_and_conf add_constReal adc2_offset {
	DATA_IN_SIZE 12 \
	DATA_OUT_SIZE 16 }
connect_proc adc2_offset s00_axi 0x70000
connect_intf redpitaya_converters_12_0 dataB_out adc2_offset data_in

add_ip_and_conf dataReal_to_ram dataReal_to_ram_1 {
	DATA_SIZE 16 \
	NB_INPUT 2 \
	NB_SAMPLE 8192 }
connect_proc dataReal_to_ram_1 s00_axi 0x80000
connect_intf adc1_offset data_out dataReal_to_ram_1 data1_in
connect_intf adc2_offset data_out dataReal_to_ram_1 data2_in
