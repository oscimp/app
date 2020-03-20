# Create instance: redpitaya_converters_0, and set properties
add_ip_and_conf redpitaya_converters redpitaya_converters_0 {
	CLOCK_DUTY_CYCLE_STABILIZER_EN {false} }
connect_to_fpga_pins redpitaya_converters_0 phys_interface phys_interface_0

# Create instance: adc2_offset, and set properties
add_ip_and_conf add_constReal adc2_offset {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }

# Create instance: adc_1_offset, and set properties
add_ip_and_conf add_constReal adc_1_offset {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }

# Create instance: adder_substracter_mod_out_pid2, and set properties
add_ip_and_conf adder_substracter_real adder_substracter_mod_out_pid2 {
	DATA_SIZE {14} }

# Create instance: adder_substracter_re_0, and set properties
add_ip_and_conf adder_substracter_real adder_substracter_re_0 {
	DATA_SIZE {14} }

# Create instance: convertComplexToReal_1, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_1 {
	DATA_SIZE {14} }

# Create instance: convertComplexToReal_2, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_2 {
	DATA_SIZE {14} }

# Create instance: convertComplexToReal_3, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_3 {
	DATA_SIZE {14}}

# Create instance: convertComplexToReal_4, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_4 {
	DATA_SIZE {14}}

# Create instance: convertComplexToReal_5, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_5 {
	DATA_SIZE {14}}

# Create instance: dac_1_offset, and set properties
add_ip_and_conf add_constReal dac_1_offset {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14}}

# Create instance: data_fast, and set properties
add_ip_and_conf dataReal_to_ram data_fast {
	DATA_SIZE {16} \
	NB_INPUT {2} \
	NB_SAMPLE {1024}}

# Create instance: data_slow, and set properties
add_ip_and_conf dataReal_to_ram data_slow {
	DATA_SIZE {16} \
	NB_INPUT {2} \
	NB_SAMPLE {2048}}

# Create instance: dds1_range, and set properties
add_ip_and_conf axi_to_dac dds1_range {
	DATA_SIZE {14} }
connect_intf redpitaya_converters_0 clk_o dds1_range ref_clk_i
connect_intf redpitaya_converters_0 rst_o dds1_range ref_rst_i

# Create instance: dds_ampl, and set properties
add_ip_and_conf add_constReal dds_ampl {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }

# Create instance: dds_ampl_mod_ampl, and set properties
add_ip_and_conf adder_substracter_real dds_ampl_mod_ampl {
	DATA_SIZE {14} }

# Create instance: dds_f0, and set properties
add_ip_and_conf add_constReal dds_f0 {
	DATA_IN_SIZE {40} \
	DATA_OUT_SIZE {40} }

# Create instance: dds_nco, and set properties
add_ip_and_conf nco_counter dds_nco {
	COUNTER_SIZE {40} \
	LUT_SIZE {12} }
connect_intf redpitaya_converters_0 clk_o dds_nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o dds_nco ref_rst_i

# Create instance: demod_mixer, and set properties
add_ip_and_conf mixer_sin demod_mixer {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} \
	NCO_SIZE {16} }

# Create instance: demod_nco, and set properties
add_ip_and_conf nco_counter demod_nco {
	COUNTER_SIZE {40} \
	DATA_SIZE {16} \
	LUT_SIZE {12} }
connect_intf redpitaya_converters_0 clk_o demod_nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o demod_nco ref_rst_i

# Create instance: dupplReal_1_to_2_1, and set properties
add_ip_and_conf dupplReal_1_to_2 dupplReal_1_to_2_1 {
	DATA_SIZE {14} }

# Create instance: dupplReal_1_to_2_2, and set properties
add_ip_and_conf dupplReal_1_to_2 dupplReal_1_to_2_2 {
	DATA_SIZE {14} }

# Create instance: dupplReal_1_to_2_3, and set properties
add_ip_and_conf dupplReal_1_to_2 dupplReal_1_to_2_3 {
	DATA_SIZE {14} }

# Create instance: dupplReal_1_to_2_4, and set properties
add_ip_and_conf dupplReal_1_to_2 dupplReal_1_to_2_4 {
	DATA_SIZE {14} }

# Create instance: dupplReal_1_to_2_5, and set properties
add_ip_and_conf dupplReal_1_to_2 dupplReal_1_to_2_5 {
	DATA_SIZE {14} }

# Create instance: expanderReal_0, and set properties
add_ip_and_conf expanderReal expanderReal_0 {
	DATA_IN_SIZE {15} \
	DATA_OUT_SIZE {14} }

# Create instance: expanderReal_5, and set properties
add_ip_and_conf expanderReal expanderReal_5 {
	DATA_IN_SIZE {15} \
	DATA_OUT_SIZE {14} }

# Create instance: expanderReal_6, and set properties
add_ip_and_conf expanderReal expanderReal_6 {
	DATA_IN_SIZE {28} \
	DATA_OUT_SIZE {34} }

# Create instance: expanderReal_7, and set properties
add_ip_and_conf expanderReal expanderReal_7 {
	DATA_IN_SIZE {15} \
	DATA_OUT_SIZE {14} }

# Create instance: firReal_0, and set properties
add_ip_and_conf firReal firReal_0 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {32} \
	DECIMATE_FACTOR {1} \
	NB_COEFF {55} }

# Create instance: meanReal_0, and set properties
add_ip_and_conf meanReal meanReal_0 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {16} \
	NB_ACCUM {128} \
	SHIFT {7} }

# Create instance: meanReal_1, and set properties
add_ip_and_conf meanReal meanReal_1 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {16} \
	NB_ACCUM {8192} \
	SHIFT {13} }

# Create instance: meanReal_2, and set properties
add_ip_and_conf meanReal meanReal_2 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {16} \
	NB_ACCUM {128} \
	SHIFT {7} }

# Create instance: meanReal_3, and set properties
add_ip_and_conf meanReal meanReal_3 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {16} \
	NB_ACCUM {8192} \
	SHIFT {13} }

# Create instance: mixer_range, and set properties
add_ip_and_conf multiplierReal mixer_range {
	DATA1_IN_SIZE 14 \
	DATA2_IN_SIZE 14 \
	DATA_OUT_SIZE 28 }

# Create instance: mixer_sin_1, and set properties
add_ip_and_conf mixer_sin mixer_sin_1 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} \
	NCO_SIZE {16} }

# Create instance: mixer_sin_3, and set properties
add_ip_and_conf mixer_sin mixer_sin_3 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} \
	NCO_SIZE {16} }

# Create instance: mixer_sin_4, and set properties
add_ip_and_conf mixer_sin mixer_sin_4 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} \
	NCO_SIZE {16} }

# Create instance: mixer_sin_dds_ampl_mod, and set properties
add_ip_and_conf mixer_sin mixer_sin_dds_ampl_mod {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }

# Create instance: mod_ampl_dds_ampl, and set properties
add_ip_and_conf axi_to_dac mod_ampl_dds_ampl
connect_intf redpitaya_converters_0 clk_o mod_ampl_dds_ampl ref_clk_i
connect_intf redpitaya_converters_0 rst_o mod_ampl_dds_ampl ref_rst_i

# Create instance: mod_ampl_dds_nco, and set properties
add_ip_and_conf nco_counter mod_ampl_dds_nco {
	COUNTER_SIZE {40} \
	DATA_SIZE {16} \
	LUT_SIZE {12} }
connect_intf redpitaya_converters_0 clk_o mod_ampl_dds_nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o mod_ampl_dds_nco ref_rst_i

# Create instance: mod_in_ampl, and set properties
add_ip_and_conf axi_to_dac mod_in_ampl
connect_intf redpitaya_converters_0 clk_o mod_in_ampl ref_clk_i
connect_intf redpitaya_converters_0 rst_o mod_in_ampl ref_rst_i

# Create instance: mod_input_nco, and set properties
add_ip_and_conf nco_counter mod_input_nco {
	COUNTER_SIZE {40} \
	DATA_SIZE {16} \
	LUT_SIZE {12} }
connect_intf redpitaya_converters_0 clk_o mod_input_nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o mod_input_nco ref_rst_i

# Create instance: mod_out_pid2_ampl, and set properties
add_ip_and_conf axi_to_dac mod_out_pid2_ampl
connect_intf redpitaya_converters_0 clk_o mod_out_pid2_ampl ref_clk_i
connect_intf redpitaya_converters_0 rst_o mod_out_pid2_ampl ref_rst_i

# Create instance: mod_out_pid2_nco, and set properties
add_ip_and_conf nco_counter mod_out_pid2_nco {
	COUNTER_SIZE {40} \
	DATA_SIZE {16} \
	LUT_SIZE {12} }
connect_intf redpitaya_converters_0 clk_o mod_out_pid2_nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o mod_out_pid2_nco ref_rst_i

# Create instance: pid1, and set properties
add_ip_and_conf pidv3_axi pid1 {
	DSR {0} \
	ISR {19} \
	I_SIZE {18} \
	PSR {13} }

# Create instance: pid2, and set properties
add_ip_and_conf pidv3_axi pid2 {
	DSR {0} \
	ISR {19} \
	I_SIZE {18} \
	PSR {13} }

# Create instance: pid2_offset, and set properties
add_ip_and_conf add_constReal pid2_offset {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }

# Create instance: pid3, and set properties
add_ip_and_conf pidv3_axi pid3 {
	DSR {0} \
	ISR {19} \
	I_SIZE {18} \
	PSR {13} }

# Create instance: piid, and set properties
add_ip_and_conf pidv3_axi piid {
	DSR {0} \
	ISR {19} \
	I_SIZE {18} \
	PSR {13} }

# Create instance: shifterReal_1, and set properties
add_ip_and_conf shifterReal shifterReal_1 {
	DATA_IN_SIZE {34} \
	DATA_OUT_SIZE {40} }

# Create instance: shifterReal_dyn_0, and set properties
add_ip_and_conf shifterReal_dyn shifterReal_dyn_0 {
	DATA_OUT_SIZE {14} }

connect_proc_rst redpitaya_converters_0 adc_rst_i

# Create interface connections
connect_intf dupplReal_1_to_2_3 data2_out mixer_range data1_in
connect_intf dds1_range dataA_out mixer_range data2_in
connect_intf mixer_range data_out expanderReal_6 data_in

connect_intf adc2_offset data_out pid3 data_in
connect_intf adc_1_offset data_out demod_mixer data_in
connect_intf dds_ampl data_out dds_ampl_mod_ampl data1_in
connect_intf dds_f0 data_out dds_nco pinc_in
connect_intf adder_substracter_mod_out_pid2 data_out expanderReal_5 data_in
connect_intf adder_substracter_re_0 data_out expanderReal_0 data_in
connect_intf mixer_sin_1 data_in mod_in_ampl dataA_out
connect_intf adder_substracter_mod_out_pid2 data2_in convertComplexToReal_1 dataI_out
connect_intf convertComplexToReal_2 dataI_out dds_ampl data_in
connect_intf convertComplexToReal_3 dataI_out dac_1_offset data_in
connect_intf adder_substracter_re_0 data2_in convertComplexToReal_4 dataI_out
connect_intf convertComplexToReal_5 dataI_out firReal_0 data_in
connect_intf pid2_offset data_out redpitaya_converters_0 dataB_in
connect_intf dac_1_offset data_out redpitaya_converters_0 dataA_in
connect_intf dds_ampl_mod_ampl data_out expanderReal_7 data_in
connect_intf convertComplexToReal_5 data_in demod_mixer data_out
connect_intf demod_mixer nco_in demod_nco sine_out
connect_intf dupplReal_1_to_2_1 data1_out dupplReal_1_to_2_4 data_in
connect_intf dupplReal_1_to_2_1 data2_out pid1 data_in
connect_intf dupplReal_1_to_2_2 data1_out dupplReal_1_to_2_5 data_in
connect_intf dupplReal_1_to_2_2 data2_out dupplReal_1_to_2_3 data_in
connect_intf dupplReal_1_to_2_3 data1_out pid2 data_in
connect_intf dupplReal_1_to_2_4 data1_out meanReal_0 data_in
connect_intf dupplReal_1_to_2_4 data2_out meanReal_1 data_in
connect_intf dupplReal_1_to_2_5 data1_out meanReal_3 data_in
connect_intf dupplReal_1_to_2_5 data2_out meanReal_2 data_in
connect_intf dupplReal_1_to_2_1 data_in expanderReal_0 data_out
connect_intf expanderReal_5 data_out pid2_offset data_in
connect_intf expanderReal_6 data_out shifterReal_1 data_in
connect_intf expanderReal_7 data_out mixer_sin_dds_ampl_mod data_in
connect_intf firReal_0 data_out shifterReal_dyn_0 data_in
connect_intf data_fast data1_in meanReal_0 data_out
connect_intf data_slow data1_in meanReal_1 data_out
connect_intf data_fast data2_in meanReal_2 data_out
connect_intf data_slow data2_in meanReal_3 data_out
connect_intf convertComplexToReal_4 data_in mixer_sin_1 data_out
connect_intf convertComplexToReal_2 data_in mixer_sin_3 data_out
connect_intf convertComplexToReal_1 data_in mixer_sin_4 data_out
connect_intf convertComplexToReal_3 data_in mixer_sin_dds_ampl_mod data_out
connect_intf mixer_sin_3 data_in mod_ampl_dds_ampl dataA_out
connect_intf mixer_sin_3 nco_in mod_ampl_dds_nco sine_out
connect_intf mixer_sin_1 nco_in mod_input_nco sine_out
connect_intf mixer_sin_4 data_in mod_out_pid2_ampl dataA_out
connect_intf mixer_sin_4 nco_in mod_out_pid2_nco sine_out
connect_intf dds_nco sine_out mixer_sin_dds_ampl_mod nco_in
connect_intf adder_substracter_mod_out_pid2 data1_in pid2 data_out
connect_intf pid1 data_out piid data_in
connect_intf dds_ampl_mod_ampl data2_in pid3 data_out
connect_intf dupplReal_1_to_2_2 data_in piid data_out
connect_intf adc_1_offset data_in redpitaya_converters_0 dataA_out
connect_intf adc2_offset data_in redpitaya_converters_0 dataB_out
connect_intf dds_f0 data_in shifterReal_1 data_out
connect_intf adder_substracter_re_0 data1_in shifterReal_dyn_0 data_out

# Create port connections
#  connect_bd_net -net dds1_range_dataA_clk_o [get_bd_pins dds1_range dataA_clk_o] [get_bd_pins mixer_range nco_clk_i
#  connect_bd_net -net dds1_range_dataA_en_o [get_bd_pins dds1_range dataA_en_o] [get_bd_pins mixer_range nco_en_i
#  connect_bd_net -net dds1_range_dataA_o [get_bd_pins dds1_range dataA_o] [get_bd_pins mixer_range nco_i_i
#  connect_bd_net -net dds1_range_dataA_rst_o [get_bd_pins dds1_range dataA_rst_o] [get_bd_pins mixer_range nco_rst_i

# Create address segments
connect_proc adc2_offset s00_axi 0x50000
connect_proc adc_1_offset s00_axi 0x10000
connect_proc dac_1_offset s00_axi 0x120000
connect_proc data_fast s00_axi 0x90000
connect_proc data_slow s00_axi 0xA0000
connect_proc dds1_range s00_axi 0xB0000
connect_proc dds_ampl s00_axi 0x1D0000
connect_proc dds_f0 s00_axi 0x30000
connect_proc dds_nco s00_axi 0x40000
connect_proc demod_nco s00_axi 0xF0000
connect_proc firReal_0 s00_axi 0x100000
connect_proc mod_ampl_dds_ampl s00_axi 0x1A0000
connect_proc mod_ampl_dds_nco s00_axi 0x1B0000
connect_proc mod_in_ampl s00_axi 0x80000
connect_proc mod_input_nco s00_axi 0x70000
connect_proc mod_out_pid2_ampl s00_axi 0xC0000
connect_proc mod_out_pid2_nco s00_axi 0x1C0000
connect_proc pid1 s00_axi 0x60000
connect_proc pid2_offset s00_axi 0x20000
connect_proc pid2 s00_axi 0xE0000
connect_proc pid3 s00_axi 0xD0000
connect_proc piid s00_axi 0x00000
connect_proc shifterReal_dyn_0 s00_axi 0x110000
