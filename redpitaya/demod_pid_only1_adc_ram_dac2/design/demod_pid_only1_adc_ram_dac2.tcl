# Create instance: redpitaya_converters_0, and set properties
add_ip_and_conf redpitaya_converters redpitaya_converters_0 {
	CLOCK_DUTY_CYCLE_STABILIZER_EN {false} }
connect_to_fpga_pins redpitaya_converters_0 phys_interface phys_interface_0

# Create instance: adc1_offset, and set properties
add_ip_and_conf add_constReal adc1_offset {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }
connect_proc adc1_offset s00_axi 0x00000

# Create instance: adc2_offset, and set properties
add_ip_and_conf add_constReal adc2_offset {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }
connect_proc adc2_offset s00_axi 0x30000

# Create instance: convertComplexToReal_0, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_0 {
	DATA_SIZE {14} }

# Create instance: convertComplexToReal_1, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_1 {
	DATA_SIZE {14} }

# Create instance: dac1_offset1, and set properties
add_ip_and_conf add_constReal dac1_offset1 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }
connect_proc dac1_offset1 s00_axi 0xE0000

# Create instance: dac2_offset, and set properties
add_ip_and_conf add_constReal dac2_offset {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }
connect_proc dac2_offset s00_axi 0x60000

# Create instance: data_adc2, and set properties
add_ip_and_conf dataReal_to_ram data_adc2 {
	DATA_SIZE {16} \
	NB_INPUT {2} }
connect_proc data_adc2 s00_axi 0x90000

# Create instance: data_fast, and set properties
add_ip_and_conf dataReal_to_ram data_fast {
	DATA_SIZE {16} \
	NB_INPUT {2} }
connect_proc data_fast s00_axi 0xB0000

# Create instance: data_proc, and set properties
add_ip_and_conf dataReal_to_ram data_proc {
	DATA_SIZE {16} \
	NB_INPUT {2} }
connect_proc data_proc s00_axi 0x100000

# Create instance: data_slow, and set properties
add_ip_and_conf dataReal_to_ram data_slow {
	DATA_SIZE {16} \
	NB_INPUT {2} }
connect_proc data_slow s00_axi 0xC0000

# Create instance: demod1_nco, and set properties
add_ip_and_conf nco_counter demod1_nco {
	COUNTER_SIZE {40} \
	LUT_SIZE {12} }
connect_intf redpitaya_converters_0 clk_o demod1_nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o demod1_nco ref_rst_i
connect_proc demod1_nco s00_axi 0x40000

# Create instance: demod2_nco, and set properties
add_ip_and_conf nco_counter demod2_nco {
	COUNTER_SIZE {40} \
	LUT_SIZE {12} }
connect_intf redpitaya_converters_0 clk_o demod2_nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o demod2_nco ref_rst_i
connect_proc demod2_nco s00_axi 0x50000

# Create instance: dupplReal_1_to_2_0, and set properties
add_ip_and_conf dupplReal_1_to_2 dupplReal_1_to_2_0 {
	DATA_SIZE {14} }

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

# Create instance: firReal_I, and set properties
add_ip_and_conf firReal firReal_I {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {32} \
	DECIMATE_FACTOR {1} \
	NB_COEFF {25} }
connect_proc firReal_I s00_axi 0x70000

# Create instance: firReal_I1, and set properties
add_ip_and_conf firReal firReal_I1 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {32} \
	DECIMATE_FACTOR {1} \
	NB_COEFF {15} }
connect_proc firReal_I1 s00_axi 0x110000

# Create instance: firReal_Q, and set properties
add_ip_and_conf firReal firReal_Q {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {32} \
	DECIMATE_FACTOR {1} \
	NB_COEFF {20} }
connect_proc firReal_Q s00_axi 0x80000

# Create instance: meanReal_0, and set properties
add_ip_and_conf meanReal meanReal_0 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }

# Create instance: meanReal_1, and set properties
add_ip_and_conf meanReal meanReal_1 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }

# Create instance: meanReal_2, and set properties
add_ip_and_conf meanReal meanReal_2 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} \
	NB_ACCUM {128} \
	SHIFT {7} }

# Create instance: meanReal_3, and set properties
add_ip_and_conf meanReal meanReal_3 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {16} \
	NB_ACCUM {16} \
	SHIFT {4} }

# Create instance: meanReal_4, and set properties
add_ip_and_conf meanReal meanReal_4 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {16} \
	NB_ACCUM {16} \
	SHIFT {4} }

# Create instance: meanReal_5, and set properties
add_ip_and_conf meanReal meanReal_5 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {16} \
	NB_ACCUM {1024} \
	SHIFT {10} }

# Create instance: meanReal_6, and set properties
add_ip_and_conf meanReal meanReal_6 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {16} \
	NB_ACCUM {1024} \
	SHIFT {10} }

# Create instance: meanReal_7, and set properties
add_ip_and_conf meanReal meanReal_7 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {16} \
	NB_ACCUM {16} \
	SHIFT {4} }

# Create instance: meanReal_8, and set properties
add_ip_and_conf meanReal meanReal_8 {
	DATA_IN_SIZE {16} \
	DATA_OUT_SIZE {16} \
	NB_ACCUM {16} \
	SHIFT {4} }

# Create instance: mixer_sin_2, and set properties
add_ip_and_conf mixer_sin mixer_sin_2 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} \
	NCO_SIZE {16} }

# Create instance: mixer_sin_3, and set properties
add_ip_and_conf mixer_sin mixer_sin_3 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }

# Create instance: pidv3_axi_0, and set properties
add_ip_and_conf pidv3_axi pidv3_axi_0 {
	DSR {0} \
	ISR {19} \
	I_SIZE {18} \
	PSR {13} }
connect_proc pidv3_axi_0 s00_axi 0xD0000

# Create instance: proc_out, and set properties
add_ip_and_conf axi_to_dac proc_out {
	DATA_SIZE {14} }
connect_intf redpitaya_converters_0 clk_o proc_out ref_clk_i
connect_intf redpitaya_converters_0 rst_o proc_out ref_rst_i
connect_proc proc_out s00_axi 0x10000

# Create instance: shifterReal_dyn_0, and set properties
add_ip_and_conf shifterReal_dyn shifterReal_dyn_0 {
	DATA_IN_SIZE {32} \
	DATA_OUT_SIZE {14} \
	DEFAULT_SHIFT {9} }
connect_proc shifterReal_dyn_0 s00_axi 0x20000

# Create instance: shifterReal_dyn_1, and set properties
add_ip_and_conf shifterReal_dyn shifterReal_dyn_1 {
	DATA_IN_SIZE {32} \
	DATA_OUT_SIZE {16} \
	DEFAULT_SHIFT {9} }
connect_proc shifterReal_dyn_1 s00_axi 0xA0000

# Create instance: shifterReal_dyn_2, and set properties
add_ip_and_conf shifterReal_dyn shifterReal_dyn_2 {
	DATA_IN_SIZE {32} \
	DATA_OUT_SIZE {16} \
	DEFAULT_SHIFT {9} }
connect_proc shifterReal_dyn_2 s00_axi 0x120000

# Create instance: switchReal_0, and set properties
add_ip_and_conf switchReal switchReal_0 {
	DATA_SIZE {16} }
connect_proc switchReal_0 s00_axi 0xF0000

# Create interface connections
connect_proc_rst redpitaya_converters_0 adc_rst_i

connect_intf adc1_offset data_out mixer_sin_2 data_in
connect_intf adc2_offset data_out mixer_sin_3 data_in
connect_intf convertComplexToReal_0 dataI_out meanReal_0 data_in
connect_intf convertComplexToReal_0 dataQ_out meanReal_1 data_in
connect_intf convertComplexToReal_1 dataI_out meanReal_2 data_in
connect_intf dac1_offset1 data_out redpitaya_converters_0 dataA_in
connect_intf dac2_offset data_out redpitaya_converters_0 dataB_in
connect_intf demod1_nco sine_out mixer_sin_2 nco_in
connect_intf demod2_nco sine_out mixer_sin_3 nco_in
connect_intf dupplReal_1_to_2_0 data1_out dupplReal_1_to_2_1 data_in
connect_intf dupplReal_1_to_2_0 data2_out meanReal_5 data_in
connect_intf dupplReal_1_to_2_1 data1_out pidv3_axi_0 data_in
connect_intf dupplReal_1_to_2_1 data2_out meanReal_3 data_in
connect_intf dupplReal_1_to_2_2 data1_out dupplReal_1_to_2_3 data_in
connect_intf dupplReal_1_to_2_2 data2_out meanReal_4 data_in
connect_intf dupplReal_1_to_2_3 data1_out meanReal_7 data_in
connect_intf dupplReal_1_to_2_3 data2_out meanReal_6 data_in
connect_intf dupplReal_1_to_2_2 data_in dupplReal_1_to_2_4 data1_out
connect_intf dac1_offset1 data_in dupplReal_1_to_2_4 data2_out
connect_intf firReal_I1 data_out shifterReal_dyn_2 data_in
connect_intf firReal_I data_out shifterReal_dyn_0 data_in
connect_intf firReal_Q data_out shifterReal_dyn_1 data_in
connect_intf firReal_I data_in meanReal_0 data_out
connect_intf firReal_Q data_in meanReal_1 data_out
connect_intf firReal_I1 data_in meanReal_2 data_out
connect_intf data_fast data1_in meanReal_3 data_out
connect_intf data_fast data2_in meanReal_4 data_out
connect_intf data_slow data1_in meanReal_5 data_out
connect_intf data_slow data2_in meanReal_6 data_out
connect_intf meanReal_7 data_out switchReal_0 data1_in
connect_intf meanReal_8 data_out switchReal_0 data2_in
connect_intf convertComplexToReal_0 data_in mixer_sin_2 data_out
connect_intf convertComplexToReal_1 data_in mixer_sin_3 data_out
connect_intf dupplReal_1_to_2_4 data_in pidv3_axi_0 data_out
connect_intf dac2_offset data_in proc_out dataA_out
connect_intf adc1_offset data_in redpitaya_converters_0 dataA_out
connect_intf adc2_offset data_in redpitaya_converters_0 dataB_out
connect_intf dupplReal_1_to_2_0 data_in shifterReal_dyn_0 data_out
connect_intf meanReal_8 data_in shifterReal_dyn_1 data_out
connect_intf data_adc2 data1_in shifterReal_dyn_2 data_out
connect_intf data_proc data1_in switchReal_0 data_out
