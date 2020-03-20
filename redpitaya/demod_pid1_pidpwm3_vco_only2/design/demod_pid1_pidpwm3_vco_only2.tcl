# Create instance: redpitaya_converters_0, and set properties
add_ip_and_conf redpitaya_converters redpitaya_converters_0 {
	CLOCK_DUTY_CYCLE_STABILIZER_EN {false} }
connect_to_fpga_pins redpitaya_converters_0 phys_interface phys_interface_0

# Create instance: adc_1_offset, and set properties
add_ip_and_conf add_constReal adc_1_offset {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }

# Create instance: adder_substracter_re_0, and set properties
add_ip_and_conf adder_substracter_real adder_substracter_re_0 {
	DATA_SIZE {14} }

# Create instance: adder_substracter_re_1, and set properties
add_ip_and_conf adder_substracter_real adder_substracter_re_1 {
	DATA_SIZE {14} }

# Create instance: adder_substracter_re_2, and set properties
add_ip_and_conf adder_substracter_real adder_substracter_re_2 {
	DATA_SIZE {14} }

# Create instance: convertComplexToReal_0, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_0 {
	DATA_SIZE {14} }

# Create instance: convertComplexToReal_1, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_1 {
	DATA_SIZE {14} }

# Create instance: convertComplexToReal_2, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_2 {
	DATA_SIZE {14} }

# Create instance: convertComplexToReal_3, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_3 {
	DATA_SIZE {14} }

# Create instance: convertComplexToReal_4, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_4 {
	DATA_SIZE {14} }

# Create instance: dac2_offset, and set properties
add_ip_and_conf add_constReal dac2_offset {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }

# Create instance: dac_1_offset, and set properties
add_ip_and_conf add_constReal dac_1_offset {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }

# Create instance: dataReal_to_ram_0, and set properties
add_ip_and_conf dataReal_to_ram dataReal_to_ram_0 {
	DATA_SIZE {14} \
	NB_INPUT {2} \
	NB_SAMPLE {128} }

# Create instance: data_fast, and set properties
add_ip_and_conf dataReal_to_ram data_fast {
	DATA_SIZE {16} \
	NB_INPUT {2} \
	NB_SAMPLE {1024} }

# Create instance: data_slow, and set properties
add_ip_and_conf dataReal_to_ram data_slow {
	DATA_SIZE {16} \
	NB_INPUT {2} \
	NB_SAMPLE {2048} }

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

# Create instance: firReal_0, and set properties
add_ip_and_conf firReal firReal_0 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {32} \
	DECIMATE_FACTOR {1} \
	NB_COEFF {55} }

# Create instance: meanReal_0, and set properties
add_ip_and_conf meanReal meanReal_0 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} \
	NB_ACCUM {8192} \
	SHIFT {13} }

# Create instance: meanReal_1, and set properties
add_ip_and_conf meanReal meanReal_1 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {16} \
	NB_ACCUM {128} \
	SHIFT {7} }

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

# Create instance: meanReal_4, and set properties
add_ip_and_conf meanReal meanReal_4 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {16} \
	NB_ACCUM {8192} \
	SHIFT {13} }

# Create instance: mixer_sin_1, and set properties
add_ip_and_conf mixer_sin mixer_sin_1 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} \
	NCO_SIZE {16} }

# Create instance: mixer_sin_2, and set properties
add_ip_and_conf mixer_sin mixer_sin_2 {
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

# Create instance: mixer_sin_5, and set properties
add_ip_and_conf mixer_sin mixer_sin_5 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }

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

# Create instance: mod_nco, and set properties
add_ip_and_conf nco_counter mod_nco {
	COUNTER_SIZE {40} \
	DATA_SIZE {16} \
	LUT_SIZE {12} }
connect_intf redpitaya_converters_0 clk_o mod_nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o mod_nco ref_rst_i

# Create instance: mod_nco_ampl, and set properties
add_ip_and_conf axi_to_dac mod_nco_ampl
connect_intf redpitaya_converters_0 clk_o mod_nco_ampl ref_clk_i
connect_intf redpitaya_converters_0 rst_o mod_nco_ampl ref_rst_i

# Create instance: mod_out_ampl, and set properties
add_ip_and_conf axi_to_dac mod_out_ampl
connect_intf redpitaya_converters_0 clk_o mod_out_ampl ref_clk_i
connect_intf redpitaya_converters_0 rst_o mod_out_ampl ref_rst_i

# Create instance: mod_out_nco1, and set properties
add_ip_and_conf nco_counter mod_out_nco1 {
	COUNTER_SIZE {40} \
	DATA_SIZE {16} \
	LUT_SIZE {12} }
connect_intf redpitaya_converters_0 clk_o mod_out_nco1 ref_clk_i
connect_intf redpitaya_converters_0 rst_o mod_out_nco1 ref_rst_i

# Create instance: mod_out_nco2, and set properties
add_ip_and_conf nco_counter mod_out_nco2 {
	COUNTER_SIZE {40} \
	DATA_SIZE {16} \
	LUT_SIZE {12} }
connect_intf redpitaya_converters_0 clk_o mod_out_nco2 ref_clk_i
connect_intf redpitaya_converters_0 rst_o mod_out_nco2 ref_rst_i

# Create instance: pid1, and set properties
add_ip_and_conf pidv3_axi pid1 {
	DSR {0} \
	ISR {19} \
	I_SIZE {18} \
	PSR {13} \
	P_SIZE {14} }

# Create instance: pid2, and set properties
add_ip_and_conf pidv3_axi pid2 {
	DSR {0} \
	ISR {19} \
	I_SIZE {18} \
	PSR {13} \
	P_SIZE {14} }

# Create instance: pwm_axi_0, and set properties
add_ip_and_conf pwm_axi pwm_axi_0 {
	COUNTER_SIZE {14} }
connect_intf redpitaya_converters_0 clk_o pwm_axi_0 ref_clk_i
connect_intf redpitaya_converters_0 rst_o pwm_axi_0 ref_rst_i
connect_to_fpga_pins pwm_axi_0 pwm_o pwm_o

# Create instance: pwm_offset, and set properties
add_ip_and_conf add_constReal pwm_offset {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }

# Create instance: shifterReal_dyn_1, and set properties
add_ip_and_conf shifterReal_dyn shifterReal_dyn_1 {
	DATA_OUT_SIZE {14} \
	DEFAULT_SHIFT {9} }

# Create interface connections
connect_proc_rst redpitaya_converters_0 adc_rst_i

connect_intf adc_1_offset data_out mixer_sin_5 data_in
connect_intf adder_substracter_re_0 data_out expanderReal_0 data_in
connect_intf adder_substracter_re_1 data_out dac_1_offset data_in
connect_intf adder_substracter_re_2 data_out pwm_offset data_in
connect_intf mixer_sin_1 data_in mod_in_ampl dataA_out
connect_intf convertComplexToReal_0 dataI_out firReal_0 data_in
connect_intf adder_substracter_re_0 data2_in convertComplexToReal_1 dataI_out
connect_intf adder_substracter_re_1 data1_in convertComplexToReal_2 dataI_out
connect_intf adder_substracter_re_2 data1_in convertComplexToReal_3 dataI_out
connect_intf convertComplexToReal_4 dataI_out dac2_offset data_in
connect_intf dac2_offset data_out redpitaya_converters_0 dataB_in
connect_intf dac_1_offset data_out redpitaya_converters_0 dataA_in
connect_intf dataReal_to_ram_0 data1_in pwm_offset data_out
connect_intf demod_nco sine_out mixer_sin_5 nco_in
connect_intf dupplReal_1_to_2_1 data1_out dupplReal_1_to_2_4 data_in
connect_intf dupplReal_1_to_2_1 data2_out pid1 data_in
connect_intf dupplReal_1_to_2_2 data1_out dupplReal_1_to_2_5 data_in
connect_intf dupplReal_1_to_2_2 data2_out dupplReal_1_to_2_3 data_in
connect_intf adder_substracter_re_1 data2_in dupplReal_1_to_2_3 data1_out
connect_intf dupplReal_1_to_2_3 data2_out meanReal_0 data_in
connect_intf dupplReal_1_to_2_4 data1_out meanReal_4 data_in
connect_intf dupplReal_1_to_2_4 data2_out meanReal_1 data_in
connect_intf dupplReal_1_to_2_5 data1_out meanReal_3 data_in
connect_intf dupplReal_1_to_2_5 data2_out meanReal_2 data_in
connect_intf dupplReal_1_to_2_1 data_in expanderReal_0 data_out
connect_intf firReal_0 data_out shifterReal_dyn_1 data_in
connect_intf meanReal_0 data_out pid2 data_in
connect_intf data_fast data1_in meanReal_1 data_out
connect_intf data_fast data2_in meanReal_2 data_out
connect_intf data_slow data2_in meanReal_3 data_out
connect_intf data_slow data1_in meanReal_4 data_out
connect_intf convertComplexToReal_1 data_in mixer_sin_1 data_out
connect_intf convertComplexToReal_2 data_in mixer_sin_2 data_out
connect_intf convertComplexToReal_3 data_in mixer_sin_3 data_out
connect_intf convertComplexToReal_4 data_in mixer_sin_4 data_out
connect_intf convertComplexToReal_0 data_in mixer_sin_5 data_out
connect_intf mixer_sin_2 data_in mod_out_ampl dataA_out
connect_intf mixer_sin_1 nco_in mod_input_nco sine_out
connect_intf mixer_sin_4 data_in mod_nco_ampl dataA_out
connect_intf mixer_sin_4 nco_in mod_nco sine_out
connect_intf mixer_sin_3 data_in mod_out_ampl dataB_out
connect_intf mixer_sin_2 nco_in mod_out_nco1 sine_out
connect_intf mixer_sin_3 nco_in mod_out_nco2 sine_out
connect_intf dupplReal_1_to_2_2 data_in pid1 data_out
connect_intf adder_substracter_re_2 data2_in pid2 data_out
connect_intf adc_1_offset data_in redpitaya_converters_0 dataA_out
connect_intf adder_substracter_re_0 data1_in shifterReal_dyn_1 data_out

# Create address segments
connect_proc dac_1_offset s00_axi 0x120000
connect_proc adc_1_offset s00_axi 0x10000
connect_proc dac2_offset s00_axi 0x20000
connect_proc pwm_offset s00_axi 0x190000
connect_proc dataReal_to_ram_0 s00_axi 0x00000
connect_proc data_fast s00_axi 0x90000
connect_proc data_slow s00_axi 0xA0000
connect_proc mod_input_nco s00_axi 0x70000
connect_proc firReal_0 s00_axi 0x50000
connect_proc mod_out_ampl s00_axi 0xB0000
connect_proc mod_in_ampl s00_axi 0x80000
connect_proc mod_out_nco1 s00_axi 0x110000
connect_proc mod_nco_ampl s00_axi 0xC0000
connect_proc mod_nco s00_axi 0x1C0000
connect_proc mod_out_nco2 s00_axi 0x1B0000
connect_proc demod_nco s00_axi 0x40000
connect_proc pid1 s00_axi 0xD0000
connect_proc pid2 s00_axi 0xE0000
connect_proc pwm_axi_0 s00_axi 0x30000
connect_proc shifterReal_dyn_1 s00_axi 0x60000
