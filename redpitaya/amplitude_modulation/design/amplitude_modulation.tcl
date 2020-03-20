## Create instance: redpitaya_converters_0, and set properties
add_ip_and_conf redpitaya_converters redpitaya_converters_0 {
	ADC_SIZE 14 \
	ADC_EN true \
	DAC_EN true }

## Create instance: AM_ampl, and set properties
add_ip_and_conf axi_to_dac AM_ampl {
	DATA_SIZE 16 \
	DATAA_DEFAULT_OUT 0 \
	DATAA_EN_ALWAYS_HIGH false \
	DATAB_DEFAULT_OUT 0 \
	DATAB_EN_ALWAYS_HIGH false \
	SYNCHRONIZE_CHAN false }
connect_proc AM_ampl s00_axi 0x00000 
connect_intf redpitaya_converters_0 clk_o AM_ampl ref_clk_i
connect_intf redpitaya_converters_0 rst_o AM_ampl ref_rst_i

##  Create instance: AM_nco, and set properties
add_ip_and_conf nco_counter AM_nco {
	COUNTER_SIZE 40 \
	DATA_SIZE 16 \
	LUT_SIZE 12 }
connect_intf redpitaya_converters_0 clk_o AM_nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o AM_nco ref_rst_i
connect_proc AM_nco s00_axi 0x40000 

## Create instance: AM_mixer_1, and set properties
add_ip_and_conf mixer_sin AM_mixer_1 {
	DATA_IN_SIZE 16 \
	NCO_SIZE 16 \
	DATA_OUT_SIZE 16 }
# am_ampl -> am_mixer1
connect_intf AM_ampl dataA_out AM_mixer_1 data_in
# am_nco -> am_mixer1
connect_intf AM_nco sine_out AM_mixer_1 nco_in

## Create instance: convertComplexToReal_0, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_0 {
	DATA_SIZE 16 }
# am_mixer1 -> convertCplx2Real
connect_intf AM_mixer_1 data_out convertComplexToReal_0 data_in

## Create instance: AM_depth, and set properties
add_ip_and_conf add_constReal AM_depth {
	DATA_OUT_SIZE 16 }
connect_proc AM_depth s00_axi 0x10000 
# am_mixer1 -> am_depth
connect_intf convertComplexToReal_0 dataI_out AM_depth data_in

## Create instance: AM_mixer_2, and set properties
add_ip_and_conf multiplierReal AM_mixer_2 {
	SIGNED_FORMAT true \
	DATA1_IN_SIZE 14 \
	DATA2_IN_SIZE 16 \
	DATA_OUT_SIZE 14 }
# ADCA -> mixer2
connect_intf redpitaya_converters_0 dataA_out AM_mixer_2 data1_in
# am_depth -> am_mixer2(data2)
connect_intf AM_depth data_out AM_mixer_2 data2_in
# am_mixer2 -> DACA
connect_intf AM_mixer_2 data_out redpitaya_converters_0 dataA_in

# Create interface connections
connect_to_fpga_pins redpitaya_converters_0 phys_interface phys_interface_0
connect_proc_rst redpitaya_converters_0 adc_rst_i
