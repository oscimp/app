# Create instance: redpitaya_converters_0, and set properties
add_ip_and_conf redpitaya_converters redpitaya_converters_0 {
	CLOCK_DUTY_CYCLE_STABILIZER_EN {false} }
connect_to_fpga_pins redpitaya_converters_0 phys_interface phys_interface_0

# Create instance: FM_nco, and set properties
add_ip_and_conf nco_counter FM_nco {
	COUNTER_SIZE {40} \
	DATA_SIZE {16} \
	LUT_SIZE {12} }
connect_intf redpitaya_converters_0 clk_o FM_nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o FM_nco ref_rst_i
connect_proc FM_nco s00_axi 0x40000

# Create instance: PM_nco, and set properties
add_ip_and_conf nco_counter PM_nco {
	COUNTER_SIZE {40} \
	LUT_SIZE {12} }
connect_intf redpitaya_converters_0 clk_o PM_nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o PM_nco ref_rst_i
connect_proc PM_nco s00_axi 0x50000

# Create instance: convertComplexToReal_0, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_0 {
	DATA_SIZE {27} }

# Create instance: convertComplexToReal_1, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_1 {
	DATA_SIZE {16} }

# Create instance: convertComplexToReal_2, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_2 {
	DATA_SIZE {14} }

# Create instance: expanderReal_2, and set properties
add_ip_and_conf expanderReal expanderReal_2 {
	DATA_IN_SIZE {27} \
	DATA_OUT_SIZE {16} }

# Create instance: expanderReal_3, and set properties
add_ip_and_conf expanderReal expanderReal_3 {
	DATA_IN_SIZE {16} \
	DATA_OUT_SIZE {12} }

# Create instance: f0, and set properties
add_ip_and_conf add_constReal f0 {
	DATA_IN_SIZE {40} \
	DATA_OUT_SIZE {40} }
connect_proc f0 s00_axi 0x60000

# Create instance: mixer_sin_0, and set properties
add_ip_and_conf mixer_sin mixer_sin_0 {
	DATA_IN_SIZE {27} \
	DATA_OUT_SIZE {27} }

# Create instance: mixer_sin_1, and set properties
add_ip_and_conf mixer_sin mixer_sin_1

# Create instance: mod_ampl, and set properties
add_ip_and_conf axi_to_dac mod_ampl {
	DATA_SIZE {27} }
connect_intf redpitaya_converters_0 clk_o mod_ampl ref_clk_i
connect_intf redpitaya_converters_0 rst_o mod_ampl ref_rst_i
connect_proc mod_ampl s00_axi 0x10000

# Create instance: nco, and set properties
add_ip_and_conf nco_counter nco {
	COUNTER_SIZE {40} \
	DATA_SIZE {14} \
	LUT_SIZE {12} }
connect_intf redpitaya_converters_0 clk_o nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o nco ref_rst_i
connect_proc nco s00_axi 0x70000

# Create instance: shifterReal_2, and set properties
add_ip_and_conf shifterReal shifterReal_2 {
	DATA_IN_SIZE {27} \
	DATA_OUT_SIZE {40}}

connect_proc_rst redpitaya_converters_0 adc_rst_i

# Create interface connections
connect_intf FM_nco sine_out mixer_sin_0 nco_in
connect_intf PM_nco sine_out mixer_sin_1 nco_in
connect_intf convertComplexToReal_0 dataI_out shifterReal_2 data_in
connect_intf convertComplexToReal_1 dataI_out expanderReal_3 data_in
connect_intf convertComplexToReal_2 dataI_out redpitaya_converters_0 dataA_in
connect_intf expanderReal_2 data_out mixer_sin_1 data_in
connect_intf expanderReal_3 data_out nco poff_in
connect_intf f0 data_out nco pinc_in
connect_intf convertComplexToReal_0 data_in mixer_sin_0 data_out
connect_intf convertComplexToReal_1 data_in mixer_sin_1 data_out
connect_intf mixer_sin_0 data_in mod_ampl dataA_out
connect_intf expanderReal_2 data_in mod_ampl dataB_out
connect_intf convertComplexToReal_2 data_in nco sine_out
connect_intf f0 data_in shifterReal_2 data_out
