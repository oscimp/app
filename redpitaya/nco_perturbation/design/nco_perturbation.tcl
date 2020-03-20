## Create instance: redpitaya_converters_0, and set properties
add_ip_and_conf redpitaya_converters redpitaya_converters_0 {
	CLOCK_DUTY_CYCLE_STABILIZER_EN false }
connect_to_fpga_pins redpitaya_converters_0 phys_interface phys_interface_0

################################################
#                                              #
# axi_to_dac                                   #
#          (A)--|                              #
#               |---|                          #
#                    multReal -->              #
# nco2 -> conv2 ----|             addSub DAC A #
#                             |->              #
#                             |                #
# ADCA -----------------------|                #
#                                              #
################################################

## Create instance: dds_ampl, and set properties
add_ip_and_conf axi_to_dac perturb_ampl {
	DATA_SIZE 14 \
	DATAA_DEFAULT_OUT 0 \
	DATAA_EN_ALWAYS_HIGH false \
	DATAB_DEFAULT_OUT 0 \
	DATAB_EN_ALWAYS_HIGH false \
	SYNCHRONIZE_CHAN false }
connect_proc perturb_ampl s00_axi 0x00000

connect_intf redpitaya_converters_0 clk_o perturb_ampl ref_clk_i
connect_intf redpitaya_converters_0 rst_o perturb_ampl ref_rst_i

## Create instance: perturb_nco, and set properties
add_ip_and_conf nco_counter perturb_nco {
	RESET_ACCUM false \
	DEFAULT_RST_ACCUM_VAL 25 \
	DATA_SIZE 16 \
	COUNTER_SIZE 40 \
	LUT_SIZE 12 }
connect_proc perturb_nco s00_axi 0x40000
connect_intf redpitaya_converters_0 clk_o perturb_nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o perturb_nco ref_rst_i

## Create instance: conv_perturb_nco, and set properties
add_ip_and_conf convertComplexToReal conv_perturb_nco {DATA_SIZE 16}
# perturb_nco -> conv_perturb_nco
connect_intf perturb_nco sine_out conv_perturb_nco data_in

## Create instance: perturb_mixer, and set properties
add_ip_and_conf multiplierReal perturb_mixer {
	DATA1_IN_SIZE 14 \
	DATA2_IN_SIZE 16 \
	DATA_OUT_SIZE 14}
# perturb_ampl(A) -> perturb_mixer(data1)
connect_intf perturb_ampl dataA_out perturb_mixer data1_in
# conv_perturb_nco(I) -> perturb_mixer(data2)
connect_intf conv_perturb_nco dataI_out perturb_mixer data2_in

## Create instance: adder_substracter_re, and set properties
add_ip_and_conf adder_substracter_real adder_substracter_re {
	format "signed" \
	opp "add" \
	DATA_SIZE 14 }
# redpitaya_converters_0(A) -> adder_substracter_re(1)
connect_intf redpitaya_converters_0 dataA_out adder_substracter_re data1_in
# perturb_mixer -> adder_substracter_re(2)
connect_intf perturb_mixer data_out adder_substracter_re data2_in
# adder_substracter_re -> redpitaya_converters_0(A)
connect_intf adder_substracter_re data_out redpitaya_converters_0 dataA_in

connect_proc_rst redpitaya_converters_0 adc_rst_i
